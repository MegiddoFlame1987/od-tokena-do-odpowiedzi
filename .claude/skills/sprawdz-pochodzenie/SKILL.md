---
name: sprawdz-pochodzenie
description: Sprawdzenie, skąd pochodzi plik albo tekst, gdy pada pytanie "czy to zrobiła AI". Czyta metadane pliku (C2PA, XMP, EXIF, bloki PNG), prowadzi przez znak wodny SynthID i pilnuje, żeby brak śladów nie został uznany za dowód. Użyj, gdy ktoś przysyła zdjęcie, nagranie, dokument albo tekst z pytaniem, czy jest prawdziwy, wygenerowany, podrobiony, albo gdy trzeba kogoś rozliczyć z użycia AI w pracy.
---

# Sprawdzanie pochodzenia

Ten skill nie wykrywa AI. Wykrywanie AI jako takie nie istnieje. Skill czyta ślady, które narzędzie zostawia w pliku, i nazywa, jak mocny jest każdy ślad.

**Zasada, której nie wolno złamać:** brak śladów nie jest dowodem na człowieka. Jeśli ktoś naciska na jednoznaczną odpowiedź przy werdykcie D, odpowiedź brzmi „nie da się ustalić” i tak zostaje.

## Co da się sprawdzić, a czego nie

| Rodzaj | Da się | Czym |
|---|---|---|
| Obraz, wideo, audio | Tak, częściowo | Metadane (ten skill) + znak wodny SynthID |
| Tekst | **Nie** | Żadne narzędzie nie daje wyniku, na którym można oprzeć decyzję wobec człowieka |

## Procedura

### Krok 1: ustal, co właściwie sprawdzamy

Zanim cokolwiek uruchomisz, zapytaj o jedną rzecz, jeśli nie wynika z rozmowy: **co się stanie po wyniku**. Rozmowa przy kawie i podstawa do rozmowy dyscyplinarnej to dwa różne progi.

Jeśli wynik ma być podstawą decyzji wobec konkretnej osoby, przeczytaj sekcję „Gdy chodzi o człowieka” na dole, zanim pójdziesz dalej.

### Krok 2: metadane (plik)

```
python3 .claude/skills/sprawdz-pochodzenie/scripts/pochodzenie.py ŚCIEŻKA [...]
```

Działa na obrazach, PNG, JPEG i na każdym pliku, w którym szuka bajtów. Dodaj `--json`, gdy wynik ma iść dalej do kodu.

Skrypt zwraca jeden z czterech werdyktów:

| Werdykt | Co znaczy | Co z tym zrobić |
|---|---|---|
| **A** | Metryczka C2PA wskazuje narzędzie AI | Potwierdź podpis na contentcredentials.org/verify. Skrypt podpisu nie sprawdza |
| **B** | Ślady AI w metadanych, bez podpisu | Poszlaka. Metadane da się dopisać ręcznie w minutę |
| **C** | Metadane aparatu, brak śladów AI | Plik ma historię. Nie wyklucza przeróbki ani podmienionego EXIF |
| **D** | Zero śladów | Najczęstszy wynik. Nie znaczy nic. Idź do kroku 3 |

Werdykt D przy pliku z Facebooka, WhatsAppa albo ze zrzutu ekranu jest normą, nie podejrzeniem. Te kanały czyszczą metadane każdemu plikowi.

### Krok 3: znak wodny (obraz, wideo, audio)

Metadane się wycina, znak wodny siedzi w samej treści. Sprawdza się go ręcznie, bo nie ma publicznego API.

1. Otwórz **https://synthid.com/** (użyj przeglądarki w sesji, jeśli jest dostępna).
2. Wgraj plik.
3. Odczytaj wynik.

Ograniczenia, o których trzeba powiedzieć od razu:

| Ograniczenie | Skutek |
|---|---|
| Czyta tylko znaki Google i partnerów (OpenAI, NVIDIA, Kakao) | Model open source przechodzi czysto |
| Około 10 sprawdzeń dziennie | Nie nadaje się do przeglądania wielu plików |
| Tekstu nie sprawdza | Nawet tekst z Gemini, choć bywa znakowany |
| Znak przetrwa kompresję, ale nie każdą przeróbkę | Mocne kadrowanie albo przerysowanie może go zdjąć |

**Wynik pozytywny** to mocny dowód, że narzędzie objęte systemem brało w tym udział. Nie mówi, czy wygenerowało całość, czy tylko poprawiło tło.

**Wynik negatywny nie znaczy nic** poza tym, że nie znaleziono znaku jednego z uczestniczących systemów.

### Krok 4: raport

Zawsze w tej kolejności, zawsze z ostatnim wierszem:

```
Plik:        nazwa
Werdykt:     litera i jedno zdanie
Ślady:       lista z mocą każdego
Sprawdzone:  metadane tak/nie, SynthID tak/nie
Czego NIE wiemy: ...
```

Ostatni wiersz jest obowiązkowy także przy werdykcie A. Zawsze czegoś nie wiemy.

## Gdy chodzi o tekst

Nie uruchamiaj żadnego detektora tekstu i nie podawaj procentów. Powody:

1. Detektory tekstu mylą się w obie strony i najczęściej oskarżają osoby piszące prostym językiem oraz piszące w języku obcym.
2. Wynik „87% AI” brzmi jak pomiar, a jest zgadywaniem. Brzmi dokładnie tak pewnie przy błędzie, jak przy trafieniu.

Zamiast detektora zaproponuj to, co faktycznie działa:

| Zamiast | Zrób |
|---|---|
| Sprawdzać tekst narzędziem | Poproś o wersje robocze, historię pliku, notatki |
| Szukać dowodu | Zapytaj autora wprost o treść: skąd ta liczba, co znaczy ten akapit |
| Rozstrzygać po fakcie | Ustal zasadę na przyszłość: co wolno, co trzeba oznaczyć |

## Gdy chodzi o człowieka

Jeśli wynik ma być podstawą rozmowy dyscyplinarnej, zarzutu albo odmowy przyjęcia pracy, powiedz wprost przed podaniem wyniku:

> Żaden z tych wyników nie jest dowodem na to, że konkretna osoba czegoś użyła. Werdykt mówi o pliku, nie o człowieku.

Przy werdykcie D nie wolno wyciągać wniosku w żadną stronę. Przy B trzeba powiedzieć, że metadane da się podrobić. Przy A i pozytywnym SynthID nadal nie wiemy, kto wgrał plik i czy wiedział, czym jest.

To nie jest ostrożność dla ostrożności. Fałszywe oskarżenie na podstawie narzędzia, które brzmi pewniej niż jest, kosztuje więcej niż niewykryte użycie AI.

## Co odświeżyć, gdy coś się zmieni

| Element | Gdzie |
|---|---|
| Nowe nazwy generatorów | Lista `GENERATORY` w `scripts/pochodzenie.py` |
| Nowi partnerzy SynthID | Tabela w kroku 3 i sekcja 3 na stronie `/wykrywanie` |
| Nowe pola metadanych | `PNG_KLUCZE_AI` i `IPTC_AI` w skrypcie |

Stan wiedzy o SynthID: 8 października 2026.
