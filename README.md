# Od tokena do odpowiedzi

Mała encyklopedia AI pod materiały szkoleniowe. Strony statyczne, zero zależności, zero builda.

## Strony

| Adres | Plik | Temat |
|---|---|---|
| `/` | `index.html` | Część pierwsza: jak działa model językowy, od tokena do produktu. 22 sekcje, 10 interaktywnych dem. |
| `/agenci` | `agenci.html` | Część druga: od zadania do agenta. Pętla, narzędzia, notatnik, uprawnienia, rodzaje, gdzie się psuje. 15 sekcji, 7 dem. |

Każda sekcja: nagłówek, jedno zdanie, jedno demo, jedna linia „sprawdzone / uproszczone". Każda strona kończy się tabelą zbiorczą tego, co można cytować dalej.

## Deploy na Vercel (3 opcje)

1. Przeglądarka: vercel.com → Add New → Project → przeciągnij ten folder.
2. CLI: `npm i -g vercel && vercel --prod` w tym folderze.
3. GitHub: wrzuć folder do repo, w Vercel „Import Git Repository", framework: Other.

`vercel.json` włącza czyste adresy, więc `agenci.html` jest dostępne jako `/agenci`.

## Dodawanie kolejnej strony

1. Skopiuj `agenci.html` jako szablon (style i helpery JS są w środku, bez wspólnego pliku CSS).
2. Zmień tytuł, hero, łańcuch części i sekcje.
3. Dodaj link w `index.html`: karta `.next` w hero, wpis w `nav.parts`, wiersz w tej tabeli.

## Wersje
- v1: łańcuch 20 sekcji, 10 interaktywnych dem.
- v2: część VI, dziesięć typów rozmów i jak model przez nie przechodzi (sekcje 21–22).
- v3: osobna strona `/agenci`, część druga materiału. Link z hero, nawigacji i sekcji 18.
