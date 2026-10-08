# Od tokena do odpowiedzi

Mała encyklopedia AI pod materiały szkoleniowe. Strony statyczne, zero zależności, zero builda.

## Zakładki

| Adres | Plik | Temat |
|---|---|---|
| `/` | `index.html` | 1. Jak działa model językowy, od tokena do produktu. 22 sekcje, 10 dem. |
| `/agenci` | `agenci.html` | 2. Od zadania do agenta. Pętla, narzędzia, notatnik, uprawnienia, gdzie się psuje. 15 sekcji, 7 dem. |
| `/warsztat` | `warsztat.html` | 3. Od czatu do warsztatu. Umiejętności, API i koszt, MCP i routery, agenci w terminalu, modele lokalne, GitHub. 16 sekcji, 8 dem. Stan na 2026-10-08. |
| `/nowosci` | `nowosci.html` | 4. Nowości. Dane w bloku `<script type="application/json" id="dane">`, strona renderuje się z niego. |

Każda sekcja: nagłówek, jedno zdanie, jedno demo, jedna linia „sprawdzone / uproszczone". Każda strona kończy się tabelą zbiorczą tego, co można cytować dalej. Każda strona ma u góry pasek zakładek `nav.tabs`.

## Umiejętności dla Claude (`.claude/skills/`)

| Umiejętność | Do czego |
|---|---|
| `tokena-redakcja` | Redakcja pod szerszą publiczność. Progi czytelności skalibrowane na v3, słownik stały, skrypt `scripts/czytelnosc.py`. |
| `tokena-pm` | Product manager: co dalej, backlog, procedura odświeżania `/nowosci`. |

Pomiar czytelności: `python3 .claude/skills/tokena-redakcja/scripts/czytelnosc.py warsztat.html --sekcje`

## Deploy na Vercel

GitHub → Vercel, framework: Other. Push na `main` idzie od razu na żywo. Zmiany robimy na gałęzi, Vercel daje podgląd, merge do `main` po akceptacji.

`vercel.json` włącza czyste adresy, więc `agenci.html` jest dostępne jako `/agenci`.

## Dodawanie kolejnej strony

1. Skopiuj `warsztat.html` jako szablon (style i helpery JS są w środku, bez wspólnego pliku CSS).
2. Zmień tytuł, hero, łańcuch części i sekcje.
3. Dodaj zakładkę w `nav.tabs` na wszystkich stronach i wiersz w tej tabeli.

## Backlog

Najwyżej 7 pozycji. Prowadzi go umiejętność `tokena-pm`.

- [S] Sprawdzić cennik GPT-6 w API i podmienić modele OpenAI w kalkulatorze `/warsztat#s7`. Zrobione, gdy: kalkulator ma ceny z datą sprawdzenia.
- [M] Redakcja `/` sekcje 6, 10, 12 (najwyższy FOG) i objaśnienie terminów fine-tuning, embedding, RAG przy pierwszym użyciu. Zrobione, gdy: skrypt pokazuje FOG sekcji ≤ 10,5 i zero terminów bez objaśnienia.
- [S] Drugie wydanie Nowości. Zrobione, gdy: wydanie 2 na `main`.
- [S] Pilotaż: jedna osoba spoza czatu przechodzi zakładkę 3. Zrobione, gdy: zapisane trzy miejsca, w których się zgubiła.

Może kiedyś: zakładka o bezpiecznym użyciu AI w firmie (polityka, dane, zgody) jako osobny moduł szkolenia.

## Wersje
- v1: łańcuch 20 sekcji, 10 interaktywnych dem.
- v2: część VI, dziesięć typów rozmów i jak model przez nie przechodzi (sekcje 21–22).
- v3: osobna strona `/agenci`, część druga materiału. Link z hero, nawigacji i sekcji 18.
- v4: zakładki na każdej stronie, `/warsztat` (część trzecia), `/nowosci` (wydanie 1), umiejętności redakcji i PM w `.claude/skills`.
