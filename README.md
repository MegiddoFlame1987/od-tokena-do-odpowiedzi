# Od tokena do odpowiedzi

Mała encyklopedia AI pod materiały szkoleniowe. Strony statyczne, zero zależności, zero builda.

## Zakładki

| Adres | Plik | Temat |
|---|---|---|
| `/` | `index.html` | 1. Jak działa model językowy, od tokena do produktu. 22 sekcje, 10 dem. |
| `/agenci` | `agenci.html` | 2. Od zadania do agenta. Pętla, narzędzia, notatnik, uprawnienia, gdzie się psuje. 15 sekcji, 7 dem. |
| `/warsztat` | `warsztat.html` | 3. Od czatu do warsztatu. Umiejętności, API i koszt, MCP i routery, agenci w terminalu, modele lokalne, GitHub. 16 sekcji, 8 dem. Stan na 2026-10-08. |
| `/wykrywanie` | `wykrywanie.html` | 4. Czy to zrobiła AI? Znak wodny, metryczka C2PA, metadane, detektory tekstu, drzewko decyzyjne. 12 sekcji, 6 dem. Stan na 2026-10-08. |
| `/nowosci` | `nowosci.html` | 5. Nowości. Dane w bloku `<script type="application/json" id="dane">`, strona renderuje się z niego. |

Każda sekcja: nagłówek, jedno zdanie, jedno demo, jedna linia „sprawdzone / uproszczone". Każda strona kończy się tabelą zbiorczą tego, co można cytować dalej. Każda strona ma u góry pasek zakładek `nav.tabs` i wpina wspólną warstwę wizualną `fx.css` + `fx.js` (tytuł składany z tokenów, pole tokenów w tle, panele rozdziałów kręcone scrollem, dema wjeżdżające przy przewijaniu). Strony działają też bez niej, a przy włączonym ograniczeniu ruchu w systemie ruch się wyłącza.

## Umiejętności dla Claude (`.claude/skills/`)

| Umiejętność | Do czego |
|---|---|
| `tokena-redakcja` | Redakcja pod szerszą publiczność. Progi czytelności skalibrowane na v3, słownik stały, skrypt `scripts/czytelnosc.py`. |
| `tokena-pm` | Product manager: co dalej, backlog, procedura odświeżania `/nowosci`. |
| `sprawdz-pochodzenie` | Realne użycie: skąd pochodzi plik. Czyta C2PA, XMP, EXIF i bloki PNG skryptem `scripts/pochodzenie.py`, prowadzi przez SynthID, pilnuje, żeby brak śladów nie stał się dowodem. |

Pomiar czytelności: `python3 .claude/skills/tokena-redakcja/scripts/czytelnosc.py warsztat.html --sekcje`

Sprawdzenie pochodzenia pliku: `python3 .claude/skills/sprawdz-pochodzenie/scripts/pochodzenie.py plik.jpg`

## Deploy na Vercel

GitHub → Vercel, framework: Other. Push na `main` idzie od razu na żywo. Zmiany robimy na gałęzi, Vercel daje podgląd, merge do `main` po akceptacji.

`vercel.json` włącza czyste adresy, więc `agenci.html` jest dostępne jako `/agenci`.

## Dodawanie kolejnej strony

1. Skopiuj `warsztat.html` jako szablon (style i helpery JS są w środku, bez wspólnego pliku CSS).
2. Zmień tytuł, hero, łańcuch części i sekcje.
3. Wepnij `<link rel="stylesheet" href="/fx.css">` w head i `<script src="/fx.js" defer></script>` przed `</body>`.
4. Dodaj zakładkę w `nav.tabs` na wszystkich stronach i wiersz w tej tabeli.

## Backlog

Najwyżej 7 pozycji. Prowadzi go umiejętność `tokena-pm`.

- [S] Sprawdzić cennik GPT-6 w API i podmienić modele OpenAI w kalkulatorze `/warsztat#s7`. Zrobione, gdy: kalkulator ma ceny z datą sprawdzenia.
- [S] Drugie wydanie Nowości. Zrobione, gdy: wydanie 2 na `main`.
- [S] Pilotaż: jedna osoba spoza czatu przechodzi zakładkę 3. Zrobione, gdy: zapisane trzy miejsca, w których się zgubiła.

- [S] Odświeżyć listę partnerów SynthID i limit dzienny na `/wykrywanie#s6` oraz w skillu `sprawdz-pochodzenie`. Zrobione, gdy: tabela ma datę sprawdzenia nie starszą niż kwartał.

Może kiedyś: zakładka o bezpiecznym użyciu AI w firmie (polityka, dane, zgody) jako osobny moduł szkolenia.

## Wersje
- v1: łańcuch 20 sekcji, 10 interaktywnych dem.
- v2: część VI, dziesięć typów rozmów i jak model przez nie przechodzi (sekcje 21–22).
- v3: osobna strona `/agenci`, część druga materiału. Link z hero, nawigacji i sekcji 18.
- v4: zakładki na każdej stronie, `/warsztat` (część trzecia), `/nowosci` (wydanie 1), umiejętności redakcji i PM w `.claude/skills`.
- v5: zakładka `/wykrywanie` (część czwarta), umiejętność `sprawdz-pochodzenie` ze skryptem czytającym metadane. Nowości przesunięte na 5.
- v6: redakcja pięciu stron pod szerszą publiczność (wszystkie sekcje FOG ≤ 10,5), wspólna warstwa wizualna `fx.css` + `fx.js`, naprawiony zdublowany nagłówek na `/wykrywanie`.
