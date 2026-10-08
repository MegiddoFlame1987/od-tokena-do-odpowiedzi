#!/usr/bin/env python3
"""Czyta pochodzenie pliku z tego, co w nim zapisano.

Nie orzeka, czy treść zrobiła AI. Czyta ślady, które generator albo aparat
zostawia w pliku, i mówi, jak mocny jest każdy ślad.

Uzycie:
    python3 pochodzenie.py plik.jpg [plik2.png ...] [--json]
"""
import json
import os
import re
import sys

# Nazwy generatorow szukane w metadanych i naglowku pliku.
GENERATORY = [
    "midjourney", "stable diffusion", "stablediffusion", "automatic1111", "comfyui",
    "dall-e", "dalle", "gpt-image", "sora", "firefly", "photoshop generative",
    "imagen", "gemini", "veo", "nano banana", "grok", "flux", "leonardo.ai",
    "ideogram", "recraft", "krea", "runway", "pika", "luma", "kling", "hailuo",
    "elevenlabs", "suno", "udio", "novelai", "seedream", "qwen-image", "wan2",
]

# IPTC digitalSourceType: slownik wartosci, ktore znacza "AI".
IPTC_AI = {
    "trainedalgorithmicmedia": "w całości wygenerowane przez model",
    "compositewithtrainedalgorithmicmedia": "złożone, część wygenerowana przez model",
    "algorithmicallyenhanced": "zmienione algorytmem",
}

# Bloki tekstowe PNG zapisywane przez narzedzia generujace.
PNG_KLUCZE_AI = {
    "parameters": "Automatic1111 / Forge: pełny prompt i ustawienia",
    "prompt": "ComfyUI: prompt w JSON",
    "workflow": "ComfyUI: cały graf generowania",
    "sd-metadata": "starsze Stable Diffusion",
    "dream": "InvokeAI",
    "comment": "NovelAI lub podobne",
}

CZYTAJ_BAJTOW = 4 * 1024 * 1024


def czytaj(sciezka):
    with open(sciezka, "rb") as f:
        return f.read(CZYTAJ_BAJTOW)


def chunki_png(dane):
    """Zwraca listę (typ, zawartosc) chunkow PNG."""
    if not dane.startswith(b"\x89PNG\r\n\x1a\n"):
        return []
    out, i = [], 8
    while i + 8 <= len(dane):
        dlugosc = int.from_bytes(dane[i:i + 4], "big")
        typ = dane[i + 4:i + 8]
        start = i + 8
        koniec = start + dlugosc
        if dlugosc < 0 or koniec > len(dane):
            break
        out.append((typ.decode("latin-1"), dane[start:koniec]))
        if typ == b"IEND":
            break
        i = koniec + 4
    return out


def tekst_png(chunki):
    """Pary klucz: wartosc z chunkow tEXt / iTXt / zTXt."""
    pary = {}
    for typ, tresc in chunki:
        if typ == "tEXt":
            if b"\x00" in tresc:
                k, v = tresc.split(b"\x00", 1)
                pary[k.decode("latin-1")] = v.decode("latin-1", "replace")
        elif typ == "iTXt":
            czesci = tresc.split(b"\x00")
            if len(czesci) >= 5:
                pary[czesci[0].decode("latin-1")] = czesci[-1].decode("utf-8", "replace")
        elif typ == "zTXt":
            if b"\x00" in tresc:
                k, reszta = tresc.split(b"\x00", 1)
                try:
                    import zlib
                    pary[k.decode("latin-1")] = zlib.decompress(reszta[1:]).decode("utf-8", "replace")
                except Exception:
                    pary[k.decode("latin-1")] = "(nie udało się rozpakować)"
    return pary


def xmp(dane):
    m = re.search(rb"<x:xmpmeta.*?</x:xmpmeta>", dane, re.S)
    if not m:
        m = re.search(rb"<rdf:RDF.*?</rdf:RDF>", dane, re.S)
    return m.group(0).decode("utf-8", "replace") if m else ""


def exif_aparat(sciezka):
    """Make i Model z EXIF, jesli PIL je widzi."""
    try:
        from PIL import Image, ExifTags
    except ImportError:
        return {}
    try:
        with Image.open(sciezka) as im:
            raw = im.getexif()
            if not raw:
                return {}
            nazwy = {v: k for k, v in ExifTags.TAGS.items()}
            out = {}
            for pole in ("Make", "Model", "Software", "DateTimeOriginal", "DateTime"):
                tag = nazwy.get(pole)
                if tag and raw.get(tag):
                    out[pole] = str(raw.get(tag)).strip("\x00 ")
            return out
    except Exception:
        return {}


def zbadaj(sciezka):
    w = {"plik": os.path.basename(sciezka), "slady": [], "werdykt": None}
    if not os.path.isfile(sciezka):
        w["blad"] = "nie ma takiego pliku"
        return w
    w["rozmiar_kb"] = round(os.path.getsize(sciezka) / 1024, 1)
    dane = czytaj(sciezka)
    niski = dane.lower()

    def slad(moc, co, skad, szczegol=""):
        w["slady"].append({"moc": moc, "co": co, "skad": skad, "szczegol": szczegol})

    # 1. C2PA / Content Credentials
    c2pa = b"c2pa" in niski and (b"jumb" in niski or b"claim_generator" in niski or b"caBX" in dane)
    if c2pa:
        gen = ""
        m = re.search(rb"claim_generator[\"':\s]*([\x20-\x7e]{3,80})", dane)
        if m:
            gen = m.group(1).decode("latin-1").strip("\"' ,:{}")
        czy_ai = any(g in gen.lower() for g in GENERATORY) or any(g in niski[:200000] for g in [b"trainedalgorithmicmedia"])
        slad("mocny" if czy_ai else "sredni",
             "metryczka C2PA (Content Credentials) w pliku",
             "struktura pliku",
             gen or "nie udało się odczytać nazwy narzędzia")
        w["c2pa"] = True
    else:
        w["c2pa"] = False

    # 2. XMP / IPTC digitalSourceType
    x = xmp(dane)
    if x:
        nx = x.lower()
        for klucz, opis in IPTC_AI.items():
            if klucz in nx:
                slad("sredni", "znacznik IPTC digitalSourceType", "XMP", opis)
                break
        m = re.search(r"CreatorTool[^>]*>([^<]{2,80})<", x) or re.search(r'CreatorTool="([^"]{2,80})"', x)
        if m:
            slad("slaby", "nazwa narzędzia w XMP", "XMP", m.group(1).strip())
    w["xmp"] = bool(x)

    # 3. Bloki tekstowe PNG
    pary = tekst_png(chunki_png(dane))
    for klucz, wartosc in pary.items():
        opis = PNG_KLUCZE_AI.get(klucz.lower())
        if opis:
            slad("sredni", f"blok tekstowy PNG „{klucz}”", "PNG tEXt/iTXt", opis)
        elif klucz.lower() in ("software", "source", "author", "creation time"):
            slad("slaby", f"blok tekstowy PNG „{klucz}”", "PNG tEXt/iTXt", wartosc[:80])
    w["png_klucze"] = sorted(pary.keys())

    # 4. EXIF: aparat albo program
    ex = exif_aparat(sciezka)
    w["exif"] = ex
    if ex.get("Make") or ex.get("Model"):
        slad("kontr", "EXIF aparatu (marka i model)", "EXIF",
             " ".join(v for v in (ex.get("Make"), ex.get("Model")) if v))
    if ex.get("Software"):
        soft = ex["Software"]
        moc = "sredni" if any(g in soft.lower() for g in GENERATORY) else "slaby"
        slad(moc, "pole Software w EXIF", "EXIF", soft)

    # 5. Nazwa generatora gdziekolwiek w naglowku pliku
    znalezione = sorted({g for g in GENERATORY if g.encode() in niski})
    if znalezione:
        juz = " ".join(s["szczegol"].lower() for s in w["slady"])
        nowe = [g for g in znalezione if g not in juz]
        if nowe:
            slad("slaby", "nazwa generatora w bajtach pliku", "surowe bajty", ", ".join(nowe))

    # Werdykt
    moce = [s["moc"] for s in w["slady"]]
    if "mocny" in moce:
        w["werdykt"] = "A"
    elif "sredni" in moce:
        w["werdykt"] = "B"
    elif "kontr" in moce and "slaby" not in moce:
        w["werdykt"] = "C"
    elif moce:
        w["werdykt"] = "B"
    else:
        w["werdykt"] = "D"
    return w


WERDYKTY = {
    "A": ("Podpisana metryczka wskazuje narzędzie AI",
          "Ten skrypt NIE sprawdza podpisu kryptograficznie. Potwierdź w contentcredentials.org/verify."),
    "B": ("Ślady AI w metadanych, bez podpisu",
          "Metadane łatwo dopisać i łatwo usunąć. To poszlaka, nie dowód."),
    "C": ("Metadane wskazują aparat, brak śladów AI",
          "Zdjęcie ma historię. To nie wyklucza przeróbki ani generowania z podmienionym EXIF."),
    "D": ("Brak jakichkolwiek śladów",
          "NIE znaczy „zrobił to człowiek”. Serwisy społecznościowe i zrzuty ekranu czyszczą metadane. To najczęstszy wynik."),
}


def wypisz(w):
    print(f"\n=== {w['plik']}")
    if w.get("blad"):
        print("  błąd:", w["blad"])
        return
    tytul, uwaga = WERDYKTY[w["werdykt"]]
    print(f"  Werdykt {w['werdykt']}: {tytul}")
    print(f"  {uwaga}")
    if w["slady"]:
        print("\n  Ślady:")
        etykieta = {"mocny": "MOCNY ", "sredni": "ŚREDNI", "slaby": "SŁABY ", "kontr": "PRZECIW"}
        for s in w["slady"]:
            szcz = f" — {s['szczegol']}" if s["szczegol"] else ""
            print(f"    [{etykieta[s['moc']]}] {s['co']} ({s['skad']}){szcz}")
    else:
        print("\n  Ślady: żadnych.")
    print("\n  Czego ten skrypt NIE sprawdził: znaku wodnego SynthID (obraz, wideo, audio)")
    print("  oraz tekstu, którego nie da się sprawdzić żadnym narzędziem.")


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    jako_json = "--json" in sys.argv
    if not args:
        print(__doc__)
        return 1
    wyniki = [zbadaj(a) for a in args]
    if jako_json:
        print(json.dumps(wyniki, ensure_ascii=False, indent=2))
    else:
        for w in wyniki:
            wypisz(w)
    return 0


if __name__ == "__main__":
    sys.exit(main())
