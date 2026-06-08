"""
Algorytm Dijkstry - najkrotsza sciezka w grafie wazonym.
Projekt z przedmiotu programowania, UP Slupsk.
"""


def dijkstra(graf, start, koniec):
    """
    Szukamy najkrotszej drogi od 'start' do 'koniec'.
    Graf to slownik: {wierzcholek: [(sasiad, waga), ...]}
    Zwraca (dlugosc, sciezka) albo (None, []) jak nie ma drogi.
    """
    # nieskonczonosc na poczatek - tak sie robi w Dijkstrze
    INF = float('inf')
    odleglosci = {w: INF for w in graf}
    odleglosci[start] = 0

    # skad przyszlismy - zeby potem odtworzyc sciezke
    poprzednik = {w: None for w in graf}

    # wierzcholki do sprawdzenia (prosta wersja - bez kolejki priorytetowej)
    nieodwiedzone = set(graf.keys())

    while nieodwiedzone:
        # bierzemy ten z najmniejsza odlegloscia
        aktualny = min(nieodwiedzone, key=lambda w: odleglosci[w])

        if odleglosci[aktualny] == INF:
            break  # reszta jest nieosiagalna

        nieodwiedzone.remove(aktualny)

        if aktualny == koniec:
            break  # juz mamy wynik, nie musimy dalej

        # patrzymy na wszystkich sasiadow
        for sasiad, waga in graf[aktualny]:
            nowa_odleglosc = odleglosci[aktualny] + waga
            if nowa_odleglosc < odleglosci[sasiad]:
                odleglosci[sasiad] = nowa_odleglosc
                poprzednik[sasiad] = aktualny

    # odtwarzamy sciezke od konca do startu
    if odleglosci[koniec] == INF:
        return None, []

    sciezka = []
    w = koniec
    while w is not None:
        sciezka.append(w)
        w = poprzednik[w]
    sciezka.reverse()

    return odleglosci[koniec], sciezka
