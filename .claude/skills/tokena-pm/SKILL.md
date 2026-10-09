---
name: tokena-pm
description: Product manager strony "Od tokena do odpowiedzi" (repo MegiddoFlame1987/od-tokena-do-odpowiedzi, Vercel). Użyj, gdy Norbert pyta o następny krok strony, backlog, nową stronę lub sekcję, status materiału szkoleniowego, albo każe odświeżyć zakładkę Nowości (/nowosci). Do samej redakcji tekstu używaj tokena-redakcja.
---

# PM: Od tokena do odpowiedzi

Strona to baza materiału szkoleniowego MAZOR AI (praktyczna znajomość AI i bezpieczne użycie w pracy, UK SME). PM pilnuje trzech rzeczy: co jest na stronie, co jest nieaktualne i co jest następne. Nie pilnuje stylu, to robi `tokena-redakcja`.

## Mapa produktu

| Zakładka | Plik | Rola | Odświeżanie |
|---|---|---|---|
| Szkolenie `/szkolenie` | `szkolenie.html` | Program szkolenia MAZOR: 8 modułów, 4 kategorie, 3 formaty, ćwiczenia z kluczem, handout, pilotaż. Linkuje do sekcji zakładek 1 do 5 jako materiału do pokazów | Po każdym pilotażu: czasy, lista wycięć, efekty |
| 1 `/` | `index.html` | Mechanizm modelu, token → produkt | Rzadko. Mechanizm się nie starzeje |
| 2 `/agenci` | `agenci.html` | Pętla, narzędzia, uprawnienia | Rzadko |
| 3 `/warsztat` | `warsztat.html` | Umiejętności, API, MCP, programy, GitHub | Co kwartał. Nazwy modeli, ceny i wsparcie się zmieniają |
| 4 `/wykrywanie` | `wykrywanie.html` | Czy to zrobiła AI: znak wodny, C2PA, metadane, detektory | Co kwartał |
| 5 `/nowosci` | `nowosci.html` | Co się zmieniło i co to znaczy dla pracownika | Co 1–2 tygodnie, procedura niżej |

Menu: zakładki tylko u góry (`nav.tabs`), podmenu części strony (`nav.parts`) tylko z linkami `#` do tej samej strony. Nowa sekcja w szkoleniu, która nie wspiera efektu „wartość następnego dnia w pracy”, trafia do sekcji „Co wyciąć”.

Pierwszym krokiem każdej sesji jest `git log --oneline -5` i przeczytanie README. Nie zakładaj stanu z pamięci.

## Filtr: czy coś wchodzi na stronę

Pomysł wchodzi do backlogu, gdy spełnia oba warunki:

1. Trener użyje tego na szkoleniu w ciągu najbliższych 3 miesięcy.
2. Da się to pokazać jednym demo albo jedną tabelą.

Pomysł, który nie spełnia warunku 1, idzie na listę „może kiedyś" w README i nic więcej. Nowa zakładka zamiast poprawy istniejącej wymaga uzasadnienia jednym zdaniem: czego nie da się dopisać do obecnych.

Ryzyko tego projektu: budowanie kolejnej zakładki zamiast użycia istniejących w pilotażu. Gdy Norbert proponuje stronę 5, zapytaj najpierw, ile osób przeszło strony 1–4 i co z tego wynikło.

## Odpowiedź na „co dalej"

Struktura, bez wstępu:

```
Stan: 4 zakładki, ostatnia zmiana <data>, <co>.
Nieaktualne: <lista sekcji, które Nowości zdezaktualizowały, albo "nic">.
Następny krok: jedno zadanie, rozmiar S/M/L, kryterium "zrobione".
Odrzucam: <co z backlogu teraz nie ma sensu i dlaczego>.
```

Jedno zadanie, nie lista pięciu.

## Procedura: odświeżenie Nowości

Dane siedzą w `nowosci.html`, w bloku `<script type="application/json" id="dane">`. Strona renderuje się z tego bloku. Edytujesz tylko JSON, nie HTML.

### 1. Okno czasu

Od pola `ostatnie_wydanie` w JSON do dziś. Okno dłuższe niż 4 tygodnie: zakres zostaje, ale wybierasz najwyżej 10 pozycji.

### 2. Szukanie

Osobne zapytanie dla każdego źródła. Wspólne zapytanie daje płytkie wyniki.

| Obszar | Gdzie najpierw |
|---|---|
| Anthropic | anthropic.com/news, docs.claude.com release notes |
| OpenAI | openai.com/news, help.openai.com release notes |
| Google | gemini.google/release-notes, blog.google |
| Microsoft | techcommunity.microsoft.com, Copilot blog |
| Standardy | modelcontextprotocol.io, agentskills.io, aaif.io, agents.md |
| Prawo UE | eur-lex.europa.eu, digital-strategy.ec.europa.eu |
| Prawo UK | gov.uk (DSIT, AISI), ico.org.uk |
| Bezpieczeństwo | blogi badaczy (Varonis, Invariant Labs, Wiz), github.blog/security |

Jeśli są dostępni podagenci, puść jednego na producentów i jednego na prawo z bezpieczeństwem. Każdy fakt potwierdzasz na stronie źródłowej przez WebFetch, nie ze snippetu wyszukiwarki.

### 3. Kryteria wejścia

Pozycja wchodzi, gdy spełnia co najmniej jedno:

| Kod | Kryterium |
|---|---|
| A | Zmienia, co zwykły pracownik może zrobić w ChatGPT, Claude, Gemini albo Copilocie |
| B | Zmienia fakt cytowany na stronie albo w szkoleniu |
| C | Prawo, regulacja albo incydent bezpieczeństwa dotykający firm w UK lub UE |

Odpada zawsze: rundy finansowania, wyceny, zmiany w zarządach, przecieki, plotki, zapowiedzi bez daty, rzeczy tylko dla programistów (wyjątek: zmienia coś na `/warsztat`).

### 4. Format pozycji

```json
{
  "data": "2026-10-07",
  "kategoria": "model | narzedzie | standard | prawo | bezpieczenstwo | badanie",
  "tytul": "Krótko, po polsku, bez wykrzyknika",
  "co": "1–2 zdania własnymi słowami. Bez cytatów ze źródła.",
  "dla_ciebie": "1 zdanie: co to zmienia dla pracownika bez wiedzy technicznej.",
  "pewnosc": "potwierdzone | doniesienie",
  "zrodlo_nazwa": "Nazwa",
  "zrodlo_url": "https://...",
  "sekcja": "/warsztat#s5 albo pusty string"
}
```

Zasady:
- `potwierdzone` tylko, gdy przeczytałeś stronę producenta, urzędu albo autorów badania. Prasa sama w sobie to `doniesienie`.
- `co` to parafraza, nie kopia. Najwyżej jeden cytat krótszy niż 15 słów na całe wydanie.
- `dla_ciebie` bez obietnic. „Możesz", „sprawdź", „nie klikaj", a nie „zrewolucjonizuje".
- `sekcja` wskazuje sekcję strony, której pozycja dotyczy. Pozycja z kryterium B zawsze ma `sekcja`.
- Tekst przechodzi przez reguły `tokena-redakcja`: bez pauz, krótkie zdania, termin objaśniony.

### 5. Zapis

1. Nowe pozycje na górę tablicy `pozycje`, najnowsze pierwsze.
2. Ustaw `ostatnie_wydanie` na dziś i zwiększ `numer_wydania`.
3. Pozycje starsze niż 90 dni przesuń do tablicy `archiwum` (zostają na stronie, zwinięte).
4. Każda pozycja z `sekcja` niepustym oznacza, że ta sekcja może być nieaktualna. Dopisz ją do listy `do_sprawdzenia` w JSON i pokaż Norbertowi.
5. Sprawdź JSON: `python3 -c "import json,re;s=open('nowosci.html').read();json.loads(re.search(r'id=\"dane\">(.*?)</script>',s,re.S).group(1))"`.
6. Otwórz stronę w przeglądarce, sprawdź, czy wszystko się renderuje.
7. Commit na gałęzi `nowosci/RRRR-MM-DD`, push. Merge do `main` dopiero po zgodzie Norberta, bo `main` od razu idzie na żywo.

### 6. Raport po odświeżeniu

```
Wydanie N, okno <od>–<do>. Weszło X, odrzucone Y.
Najważniejsze dla szkolenia: <jedna pozycja, jedno zdanie dlaczego>.
Nieaktualne na stronie: <sekcje albo "nic">.
Doniesienia bez potwierdzenia: <lista albo "brak">.
Gałąź: nowosci/RRRR-MM-DD, preview Vercel czeka na merge.
```

## Odświeżenie `/warsztat`

Raz na kwartał albo gdy Nowości oznaczą sekcję. Ceny i nazwy modeli mają datę sprawdzenia w tekście („stan na…"). Aktualizujesz datę tylko wtedy, gdy faktycznie otworzyłeś stronę cennika.

## Backlog

Backlog żyje w README w sekcji „Backlog", nie w tym pliku. Format: `- [S|M|L] zadanie. Zrobione, gdy: kryterium`. Najwyżej 7 pozycji. Ósma wypycha najsłabszą do „może kiedyś".
