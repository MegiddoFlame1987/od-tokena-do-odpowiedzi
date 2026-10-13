# Od tokena do odpowiedzi

Mała encyklopedia AI pod materiały szkoleniowe. Strony statyczne, zero zależności, zero builda.

## Zakładki

Materiał jest tylko po angielsku. Polska wersja została usunięta 13 października 2026; leży w historii, commit `bd8346f`, znacznik `pl-v6.2`.

| Adres | Plik | Temat |
|---|---|---|
| `/training` | `training.html` | MAZOR AI Training v1.0: 8 modułów w 4 kategoriach, formaty 2h, pół dnia, cały dzień, ćwiczenia z kluczem, handout do druku, plan pilotażu. 19 sekcji, 9 dem. |
| `/` | `index.html` | 1. From Token to Answer. Jak działa model językowy, od tokena do produktu. 22 sekcje, 10 dem. |
| `/agents` | `agents.html` | 2. From Task to Agent. Pętla, narzędzia, notatnik, uprawnienia, gdzie się psuje. 15 sekcji, 7 dem. |
| `/workshop` | `workshop.html` | 3. From Chat to Workshop. Umiejętności, API i koszt, MCP i routery, agenci w terminalu, modele lokalne, GitHub. 16 sekcji, 8 dem. Stan na 2026-10-08. |
| `/detection` | `detection.html` | 4. Did AI Make This? Znak wodny, metryczka C2PA, metadane, detektory tekstu, drzewko decyzyjne. 12 sekcji, 6 dem. Stan na 2026-10-08. |
| `/news` | `news.html` | 5. What Changed. Dane w bloku `<script type="application/json" id="dane">`, strona renderuje się z niego. |

To README i umiejętności w `.claude/skills/` zostają po polsku: to warsztat, nie produkt. Po angielsku jest tylko to, co widzi czytelnik.

Każda sekcja: nagłówek, jedno zdanie, jedno demo, jedna linia „sprawdzone / uproszczone". Każda strona kończy się tabelą zbiorczą tego, co można cytować dalej. Każda strona ma u góry pasek zakładek `nav.tabs` i wpina wspólną warstwę wizualną `fx.css` + `fx.js` (tytuł składany z tokenów, pole tokenów w tle, panele rozdziałów kręcone scrollem, dema wjeżdżające przy przewijaniu). Strony działają też bez niej, a przy włączonym ograniczeniu ruchu w systemie ruch się wyłącza.

## Umiejętności dla Claude (`.claude/skills/`)

| Umiejętność | Do czego |
|---|---|
| `tokena-redakcja` | Redakcja pod szerszą publiczność. Progi czytelności skalibrowane na v3, słownik stały, skrypt `scripts/czytelnosc.py`. |
| `tokena-pm` | Product manager: co dalej, backlog, procedura odświeżania `/news`. |
| `sprawdz-pochodzenie` | Realne użycie: skąd pochodzi plik. Czyta C2PA, XMP, EXIF i bloki PNG skryptem `scripts/pochodzenie.py`, prowadzi przez SynthID, pilnuje, żeby brak śladów nie stał się dowodem. |

Pomiar czytelności: `python3 .claude/skills/tokena-redakcja/scripts/czytelnosc.py workshop.html --sekcje`

Sprawdzenie pochodzenia pliku: `python3 .claude/skills/sprawdz-pochodzenie/scripts/pochodzenie.py plik.jpg`

## Deploy na Vercel

GitHub → Vercel, framework: Other. Push na `main` idzie od razu na żywo. Zmiany robimy na gałęzi, Vercel daje podgląd, merge do `main` po akceptacji.

`vercel.json` włącza czyste adresy, więc `agents.html` jest dostępne jako `/agents`. Trzyma też 7 przekierowań 301 ze starych adresów: `/en/*` oraz polskie `/agenci`, `/warsztat`, `/wykrywanie`, `/nowosci`, `/szkolenie`.

## Dodawanie kolejnej strony

1. Skopiuj `workshop.html` jako szablon (style i helpery JS są w środku, bez wspólnego pliku CSS).
2. Zmień tytuł, hero, łańcuch części i sekcje.
3. Wepnij `<link rel="stylesheet" href="/fx.css">` w head i `<script src="/fx.js" defer></script>` przed `</body>`.
4. Dodaj zakładkę w `nav.tabs` na wszystkich stronach i wiersz w tej tabeli.
5. Pisz po angielsku. W łańcuchach JS w apostrofach nie wolno używać angielskiego apostrofu (`do not` zamiast `don't`), bo rozwala plik. Zero pauz i półpauz.

Kontrola nowej strony, wszystkie trzy muszą przejść:

```
python3 -c "import re,sys;open('/tmp/s.js','w').write(re.search(r'<script>(.*?)</script>',open(sys.argv[1],encoding='utf-8').read(),re.S).group(1))" STRONA.html && node --check /tmp/s.js
python3 -c "import re,sys;s=open(sys.argv[1],encoding='utf-8').read();print('pl:',len(re.findall(r'[ąćęłńóśźżĄĆĘŁŃÓŚŹŻ]',s)),'pauzy:',s.count(chr(8212))+s.count(chr(8211)))" STRONA.html
```

## Backlog

Najwyżej 7 pozycji. Prowadzi go umiejętność `tokena-pm`.

- [S] Sprawdzić cennik GPT-6 w API i podmienić modele OpenAI w kalkulatorze `/workshop#s7`. Zrobione, gdy: kalkulator ma ceny z datą sprawdzenia.
- [M] Zdecydować, co z pomiarem czytelności po angielsku: dopisać metrykę angielską do `czytelnosc.py` i skalibrować na obecnych stronach, albo zrezygnować z liczb. Zrobione, gdy: `tokena-redakcja` ma progi, które da się sprawdzić skryptem, albo jawnie ich nie ma.
- [S] Drugie wydanie Nowości. Zrobione, gdy: wydanie 2 na `main`.
- [M] Pilotaż szkolenia, pół dnia, 5 do 15 osób. Zrobione, gdy: ankiety zebrane i czasy w `/training#s5` poprawione według pomiaru.
- [S] Pakiet fikcyjnych dokumentów i kluczy do ćwiczeń (raport czysty i z ukrytą instrukcją, notatki do handover, SOP z 4 błędami). Zrobione, gdy: pliki w repo w folderze `cwiczenia/`.

- [S] Odświeżyć listę partnerów SynthID i limit dzienny na `/detection#s6` oraz w skillu `sprawdz-pochodzenie`. Zrobione, gdy: tabela ma datę sprawdzenia nie starszą niż kwartał.

Może kiedyś: osobny moduł szkolenia o polityce AI w firmie (dla zarządu).

## Wersje
- v1: łańcuch 20 sekcji, 10 interaktywnych dem.
- v2: część VI, dziesięć typów rozmów i jak model przez nie przechodzi (sekcje 21–22).
- v3: osobna strona `/agenci`, część druga materiału. Link z hero, nawigacji i sekcji 18.
- v4: zakładki na każdej stronie, `/warsztat` (część trzecia), `/nowosci` (wydanie 1), umiejętności redakcji i PM w `.claude/skills`.
- v5: zakładka `/wykrywanie` (część czwarta), umiejętność `sprawdz-pochodzenie` ze skryptem czytającym metadane. Nowości przesunięte na 5.
- v6: redakcja pięciu stron pod szerszą publiczność (wszystkie sekcje FOG ≤ 10,5), wspólna warstwa wizualna `fx.css` + `fx.js`, naprawiony zdublowany nagłówek na `/wykrywanie`.
- v6.1: zakładka `/szkolenie` (program MAZOR AI 1.0), jedno menu u góry, podmenu bez paska przewijania, tekst bez formy „my”, reguła osoby w `tokena-redakcja`.
- v6.2: wersja angielska wszystkich sześciu zakładek w `en/`, przełącznik PL/EN na pasku zakładek, `lang` w `<html>`, poprawiona numeracja zakładki w stopce Nowości.
- v7: tylko angielski. Strony z `en/` przeniesione do katalogu głównego, polskie usunięte (historia: znacznik `pl-v6.2`), przełącznik języka zdjęty, komentarze w `fx.js` i `fx.css` po angielsku, 7 przekierowań 301 w `vercel.json`.
