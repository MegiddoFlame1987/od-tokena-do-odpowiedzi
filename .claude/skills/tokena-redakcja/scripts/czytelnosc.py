#!/usr/bin/env python3
"""Czytelnosc stron "Od tokena do odpowiedzi".

Uzycie:
  python3 czytelnosc.py strona.html [--sekcje]   # cala strona albo sekcja po sekcji
  python3 czytelnosc.py --tekst "wklejony akapit"

Liczy tylko tekst czytany przez odbiorce (p, td, li, h2, h3, .status, .note),
bez skryptow i stylow. Zero zaleznosci poza standardowa biblioteka.

Metryki:
  zd_sr     srednia dlugosc zdania w slowach
  zd_dl%    odsetek zdan dluzszych niz 25 slow
  trudne%   odsetek slow z 4+ sylabami (przyblizenie FOG-PL, sylaby = grupy samoglosek)
  fog       FOG-PL = 0.4 * (zd_sr + trudne%)   (ok. 9 = liceum, 12 = studia)
  ang       slowa angielskie / zargon z listy ZARGON, ktore nie maja polskiego objasnienia obok
  pauzy     liczba polpauz i pauz (strona ich nie uzywa)
"""
import re, sys, html
from html.parser import HTMLParser

SAMOGLOSKI = "aąeęioóuyAĄEĘIOÓUY"
ZARGON = ["API", "MCP", "SDK", "CLI", "token", "prompt", "endpoint", "framework", "workflow",
          "repozytorium", "repo", "commit", "pull request", "README", "JSON", "embedding",
          "fine-tuning", "RAG", "LLM", "deploy", "open source", "skill", "plugin", "serwer",
          "klucz API", "rate limit", "kontekst", "harness", "terminal", "exe"]
CZYTANE = {"p", "td", "th", "li", "h1", "h2", "h3", "div"}


class P(HTMLParser):
    def __init__(self):
        super().__init__()
        self.skip = 0
        self.buf = []
        self.sekcje = []  # (id, tekst)
        self.cur = ["_poczatek", []]

    def handle_starttag(self, tag, a):
        a = dict(a)
        if tag in ("script", "style", "svg", "nav"):
            self.skip += 1
        if tag == "section" and a.get("id"):
            self.sekcje.append((self.cur[0], " ".join(self.cur[1])))
            self.cur = [a["id"], []]
        if tag in CZYTANE or tag == "br":
            self.cur[1].append("\n")

    def handle_endtag(self, tag):
        if tag in ("script", "style", "svg", "nav"):
            self.skip -= 1
        if tag in CZYTANE:
            self.cur[1].append(".\n")

    def handle_data(self, d):
        if not self.skip and d.strip():
            self.cur[1].append(d.strip())

    def koniec(self):
        self.sekcje.append((self.cur[0], " ".join(self.cur[1])))
        return self.sekcje


def sylaby(w):
    return max(1, len(re.findall(r"[%s]+" % SAMOGLOSKI, w)))


def metryki(t):
    t = html.unescape(t)
    pauzy = t.count("—") + t.count("–")
    zdania = [z.strip() for z in re.split(r"[.!?:;]+\s|\n", t) if len(z.split()) >= 3]
    slowa = re.findall(r"[A-Za-zĄĆĘŁŃÓŚŹŻąćęłńóśźż-]+", t)
    if not zdania or not slowa:
        return None
    dl = [len(z.split()) for z in zdania]
    trudne = sum(1 for w in slowa if sylaby(w) >= 4)
    zd_sr = sum(dl) / len(dl)
    tr = 100 * trudne / len(slowa)
    nisko = t.lower()
    ang = sorted({z for z in ZARGON if re.search(r"(?<![\w-])%s(?![\w-])" % re.escape(z.lower()), nisko)})
    return {
        "slow": len(slowa), "zdan": len(dl), "zd_sr": round(zd_sr, 1),
        "zd_dl%": round(100 * sum(1 for d in dl if d > 25) / len(dl), 1),
        "trudne%": round(tr, 1), "fog": round(0.4 * (zd_sr + tr), 1),
        "ang": ang, "pauzy": pauzy,
        "najdluzsze": sorted(zdania, key=lambda z: -len(z.split()))[:3],
    }


def drukuj(nazwa, m):
    if not m:
        return
    print(f"{nazwa:<14} slow {m['slow']:>5}  zd_sr {m['zd_sr']:>5}  zd_dl% {m['zd_dl%']:>5}  "
          f"trudne% {m['trudne%']:>5}  fog {m['fog']:>5}  pauzy {m['pauzy']}")


if __name__ == "__main__":
    a = sys.argv[1:]
    if not a:
        print(__doc__); sys.exit(1)
    if a[0] == "--tekst":
        m = metryki(" ".join(a[1:])); drukuj("tekst", m)
        if m:
            print("zargon:", ", ".join(m["ang"]) or "brak")
            for z in m["najdluzsze"]:
                print(" -", len(z.split()), "slow:", z[:140])
        sys.exit(0)
    p = P(); p.feed(open(a[0], encoding="utf-8").read()); sek = p.koniec()
    if "--sekcje" in a:
        for sid, t in sek:
            drukuj(sid, metryki(t))
    calosc = metryki(" ".join(t for _, t in sek))
    print("-" * 90); drukuj("CALOSC", calosc)
    print("zargon na stronie:", ", ".join(calosc["ang"]))
    print("najdluzsze zdania:")
    for z in calosc["najdluzsze"]:
        print(" -", len(z.split()), "slow:", z[:160])
