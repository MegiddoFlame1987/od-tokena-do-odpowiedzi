---
name: tokena-redakcja
description: Redakcja stron "Od tokena do odpowiedzi" (repo MegiddoFlame1987/od-tokena-do-odpowiedzi) pod szerszą publiczność. Użyj, gdy Norbert prosi o redakcję, uproszczenie, sprawdzenie czytelności, ocenę sekcji albo pisze nową sekcję lub stronę tego materiału. Nie używaj do innych tekstów.
---

# Redakcja: Od tokena do odpowiedzi

Cel: strona ma być zrozumiała dla pracownika biurowego, kierownika zmiany albo właściciela małej firmy w UK, który nigdy nie pisał kodu. Nie dla naukowca i nie dla kogoś, kto boi się komputera. Środek.

Redaktor nie dodaje treści. Usuwa przeszkody między czytelnikiem a mechanizmem.

## Kiedy redakcja jest skończona

Sekcja przechodzi, gdy spełnia wszystkie pięć warunków. Każdy da się sprawdzić.

| # | Warunek | Jak sprawdzić |
|---|---|---|
| 1 | Struktura sekcji nietknięta | Numer `k`, nagłówek h3, jedno-dwa zdania wstępu, jedno demo albo tabela, jedna linia `.status` |
| 2 | Liczby w progach (tabela niżej) | `python3 scripts/czytelnosc.py plik.html --sekcje` |
| 3 | Każdy termin z listy zargonu wyjaśniony przy pierwszym użyciu na stronie | Wynik `zargon` ze skryptu, potem ręcznie: czy obok stoi polskie objaśnienie |
| 4 | Linia statusu mówi zwykłym językiem, co jest pewne | Czytelnik bez wiedzy technicznej umie ją powtórzyć jednym zdaniem |
| 5 | Ani jednej pauzy, półpauzy ani zwrotu z listy zakazanej | Skrypt liczy pauzy, resztę grep |

## Progi

Skalibrowane na stronach v3 (8 października 2026), tą samą metodą co skrypt. To nie norma z podręcznika, tylko poziom, który materiał już trzyma. Nowy tekst nie może być gorszy od starego.

| Metryka | `/` (v3) | `/agenci` (v3) | Próg sekcji | Próg strony |
|---|---|---|---|---|
| FOG-PL | 6,8 | 7,8 | ≤ 10,5 | ≤ 8,0 |
| Średnie zdanie, słowa | 6,4 | 7,0 | ≤ 9 | ≤ 8 |
| Zdania > 25 słów | 0% | 0,4% | 0 | ≤ 1% |
| Słowa 4+ sylab | 10,6% | 12,5% | ≤ 18% | ≤ 13% |
| Pauzy | 0 | 0 | 0 | 0 |

Najgorsze sekcje v3 to `/` s6 (FOG 11,1), s12 (10,8), `/agenci` s14 (10,4). Jeśli redagujesz stare strony, zacznij od nich.

Ograniczenie metryki: komórka tabeli liczy się jak zdanie, więc sekcje z tabelami wychodzą łagodniej. FOG mierzy długość, nie zrozumienie. Warunek 3 i 4 sprawdzasz głową.

## Zasady redakcji, w kolejności ważności

1. **Termin przed użyciem.** Pierwsze wystąpienie słowa z listy zargonu na stronie dostaje objaśnienie w tym samym zdaniu albo zaraz po nim. Wzór z v3: „Narzędzie to funkcja z opisem." Potem słowo działa bez objaśnienia. Lista w `scripts/czytelnosc.py`, zmienna `ZARGON`. Dopisuj nowe terminy, gdy się pojawią.
2. **Słownik stały.** Te same rzeczy tymi samymi słowami na wszystkich stronach. Tabela niżej. Nie wprowadzaj synonimu dla urozmaicenia.
3. **Przykład z pracy, nie z laboratorium.** Linia produkcyjna, magazyn, raport zmianowy, faktura, grafik, mail do klienta. Wzór: demo pętli w `/agenci` liczy przestoje linii 3. Nie: „przykład: funkcja foo".
4. **Jedno zdanie, jedna myśl.** Zdanie z „który", „a także" i przecinkiem rozbij na dwa.
5. **Angielski tylko, gdy czytelnik go spotka na ekranie.** „API", „MCP", „README" zostają, bo tak je zobaczy w produkcie. Obok polskie objaśnienie. Angielskie słowo, którego nie zobaczy, zamieniasz na polskie.
6. **Status po ludzku.** Etykiety tylko z tego zestawu: Sprawdzone, Uproszczone, Logiczne, Praktyczne, Niesprawdzone, Następny krok. „Sprawdzone" znaczy: mechanizm albo konsensus inżynierski, z dokumentacji lub pomiaru. Nigdy nie podnoś „Logiczne" do „Sprawdzone" przy redakcji.
7. **Liczby zostają liczbami.** „Trzy na cztery" zamiast „większość". Bez zaokrąglania w górę dla efektu.
8. **Osoba tylko tam, gdzie jest potrzebna.** Bez formy „my": nie „co sprawdzamy", „jak wybieramy", „nie używamy", tylko „co jest sprawdzane", „jak powstaje lista", „nie używa się". Tekst opisowy (nagłówki, statusy, tabele, opis mechanizmu) pisany bez osoby: „Model czyta okno", „Wynik wraca do okna". Zwrot do czytelnika („Ty", tryb rozkazujący: „kliknij", „sprawdź", „nie wklejaj") tylko tam, gdzie czytelnik coś robi: polecenie w demie, zasada do zastosowania w pracy, pytanie do niego samego. Nie mieszać osób w jednym akapicie. Skrypt wypisuje kandydatów na formę „my" w linii `forma my`; każdy sprawdzasz ręcznie, bo końcówka -emy łapie też rzeczowniki (systemy, problemy).

## Słownik stały

| Mówimy | Nie mówimy | Objaśnienie przy pierwszym użyciu |
|---|---|---|
| okno kontekstu, okno | pamięć robocza, bufor | wszystko, co model widzi w jednej chwili |
| wagi | parametry (poza s. o skali) | liczby, w których zapisane jest to, czego model się nauczył |
| token | słowo, znak | kawałek tekstu, na który model tnie zdanie |
| narzędzie | funkcja, plugin | funkcja z opisem, którą program uruchamia na prośbę modelu |
| notatnik | pamięć agenta (jako nazwa części) | to, co agent zapisuje, żeby nie zapomnieć |
| uprawnienia | dostępy, permissions | co wolno zrobić bez pytania człowieka |
| agent | bot, AI (jako rzeczownik) | model w pętli, z narzędziami i warunkiem stopu |
| workflow | proces automatyczny | kolejność kroków zapisana z góry przez człowieka |
| umiejętność (skill) | prompt systemowy | folder z instrukcją, który model wczytuje, gdy zadanie pasuje |
| API | interfejs (bez dopowiedzenia) | sposób, w jaki program rozmawia z modelem bez okna czatu |

Rozszerzaj tabelę, gdy dochodzi nowa strona. Zmiana istniejącego wiersza wymaga zgody Norberta, bo zmienia wszystkie strony naraz.

## Zakazane

Pauzy (—) i półpauzy (–) w tekście czytelnika. Zwroty: „warto zauważyć", „należy podkreślić", „zanurzmy się", „kluczowe jest". Wykrzykniki. Pytania retoryczne w nagłówkach. Obietnice wyników („zaoszczędzisz 40% czasu") bez źródła i etykiety Niesprawdzone.

## Procedura

1. Uruchom skrypt na pliku z `--sekcje`: `python3 .claude/skills/tokena-redakcja/scripts/czytelnosc.py <plik> --sekcje` z katalogu repo (sklonuj repo, jeśli go nie ma). Zapisz wyniki przed.
2. Wypisz sekcje poza progiem i terminy bez objaśnienia. To jest lista robocza, pokaż ją krótko.
3. Redaguj tylko tekst czytelnika: `p`, `td`, `li`, nagłówki, `.status`, teksty w tablicach JS dem (stringi w `<script>`). Nie ruszaj CSS, struktury HTML, logiki dem, identyfikatorów `id`.
4. Uruchom skrypt ponownie. Pokaż tabelę przed i po dla zmienionych sekcji.
5. Otwórz stronę w przeglądarce i kliknij każde demo, którego teksty zmieniłeś. Dłuższy tekst potrafi rozjechać SVG.
6. Wynik oddaj jako diff albo commit na gałęzi, nigdy prosto na `main`. `main` to wersja na żywo na Vercelu.

## Format odpowiedzi

Najpierw najsłabsze miejsce, potem reszta. Krótko:

```
Najsłabsze: s12, FOG 10,8, trzy terminy bez objaśnienia (fine-tuning, embedding, RAG).
Poprawione: 6 sekcji. Strona FOG 6,8 → 6,4. Zargon bez objaśnienia: 4 → 0.
Nie ruszałem: s22, tabela rozmów, bo tam terminy są celowo w tekście przykładów.
Gałąź: redakcja/2026-10-xx
```

## Pisanie nowej sekcji

Ten sam skill, odwrotny kierunek. Szkielet:

```html
<section class="s" id="sN">
<div class="k">N / M</div><h3>Nazwa rzeczy, nie pytanie</h3>
<p>Jedno zdanie: co to jest. Drugie: dlaczego czytelnik ma się tym przejąć. Opcjonalnie trzecie: co zrobić w demo.</p>
<div class="demo">...</div>   <!-- albo <div class="tbl"><table>...</table></div> -->
<div class="status"><b>Sprawdzone:</b> ... <b>Uproszczone:</b> ...</div>
</section>
```

Każde twierdzenie z etykietą Sprawdzone potrzebuje źródła, które można pokazać, gdy ktoś zapyta. Jeśli go nie ma, etykieta to Logiczne.
