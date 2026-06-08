# Algorytm Dijkstry - projekt Python

Aplikacja z interfejsem graficznym do budowania grafu nieskierowanego i wyszukiwania najkrótszej drogi algorytmem Dijkstry.

**Autorzy:** Patryk Abel, Aleksander Korsak  
**Kierunek:** Inżynieria cyberprzestrzeni, Uniwersytet Pomorski w Słupsku

## Uruchomienie

```bash
python app.py
```

Wymagany Python 3.x z modułem `tkinter` (jest domyślnie w większości instalacji).

## Co robi aplikacja

- budowanie grafu - dodawanie wierzchołków i krawędzi z wagami
- wyświetlanie **listy sąsiedztwa** i **macierzy sąsiedztwa**
- wybór wierzchołka startowego i docelowego (lista lub kliknięcie na grafie)
- obliczanie najkrótszej drogi algorytmem Dijkstry
- wizualizacja grafu z zaznaczoną znalezioną ścieżką

## Pliki

| Plik | Opis |
|------|------|
| `app.py` | Interfejs graficzny (Tkinter) |
| `dijkstra.py` | Implementacja algorytmu Dijkstry |
| `graf.py` | Klasa grafu - lista i macierz sąsiedztwa |

## Prezentacja

Po uruchomieniu wczytuje się przykładowy graf. Kliknij **„Oblicz najkrótszą drogę"** - wynik pojawi się po lewej, a ścieżka zostanie podświetlona na rysunku grafu.
