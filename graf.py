"""
Klasa Graf - lista sasiedztwa i macierz sasiedztwa.
Graf nieskierowany, krawedzie maja wagi.
"""


class Graf:
    def __init__(self):
        self.wierzcholki = []          # lista nazw wierzcholkow
        self.krawedzie = []            # [(a, b, waga), ...]
        self.lista_sasiedztwa = {}     # slownik listy sasiedztwa

    def dodaj_wierzcholek(self, nazwa):
        """Dodaje nowy wierzcholek jesli jeszcze go nie ma."""
        nazwa = str(nazwa).strip()
        if nazwa and nazwa not in self.wierzcholki:
            self.wierzcholki.append(nazwa)
            self.lista_sasiedztwa[nazwa] = []
            self._przelicz_liste()
        return nazwa

    def dodaj_krawedz(self, a, b, waga):
        """Dodaje krawedz miedzy a i b (graf nieskierowany)."""
        a, b = str(a).strip(), str(b).strip()
        waga = float(waga)

        self.dodaj_wierzcholek(a)
        self.dodaj_wierzcholek(b)

        if a == b:
            return False  # petla - nie dodajemy

        # sprawdzamy czy juz jest taka krawedz
        for k in self.krawedzie:
            if (k[0] == a and k[1] == b) or (k[0] == b and k[1] == a):
                k[2] = waga  # aktualizujemy wage
                self._przelicz_liste()
                return True

        self.krawedzie.append((a, b, waga))
        self._przelicz_liste()
        return True

    def _przelicz_liste(self):
        """Buduje liste sasiedztwa na podstawie krawedzi."""
        self.lista_sasiedztwa = {w: [] for w in self.wierzcholki}
        for a, b, waga in self.krawedzie:
            self.lista_sasiedztwa[a].append((b, waga))
            self.lista_sasiedztwa[b].append((a, waga))

    def macierz_sasiedztwa(self):
        """
        Zwraca macierz sasiedztwa jako liste list.
        INF tam gdzie nie ma krawedzi.
        """
        n = len(self.wierzcholki)
        INF = float('inf')
        macierz = [[INF] * n for _ in range(n)]

        for i in range(n):
            macierz[i][i] = 0

        for a, b, waga in self.krawedzie:
            i = self.wierzcholki.index(a)
            j = self.wierzcholki.index(b)
            macierz[i][j] = waga
            macierz[j][i] = waga  # nieskierowany

        return macierz

    def tekst_listy(self):
        """Lista sasiedztwa jako tekst do wyswietlenia."""
        if not self.wierzcholki:
            return "(brak wierzcholkow)"

        linie = []
        for w in self.wierzcholki:
            sasiedzi = self.lista_sasiedztwa.get(w, [])
            if sasiedzi:
                opis = ", ".join(f"{s}({wg})" for s, wg in sasiedzi)
            else:
                opis = "-"
            linie.append(f"  {w} -> {opis}")
        return "\n".join(linie)

    def tekst_macierzy(self):
        """Macierz sasiedztwa jako tekst (ladnie sformatowana)."""
        if not self.wierzcholki:
            return "(brak wierzcholkow)"

        macierz = self.macierz_sasiedztwa()
        naglowek = "     " + "  ".join(f"{w:>5}" for w in self.wierzcholki)
        linie = [naglowek]

        for i, w in enumerate(self.wierzcholki):
            wiersz = []
            for j in range(len(self.wierzcholki)):
                val = macierz[i][j]
                if val == float('inf'):
                    wiersz.append("  inf")
                else:
                    wiersz.append(f"{val:5.0f}")
            linie.append(f"  {w:>3} " + "  ".join(wiersz))

        return "\n".join(linie)

    def wyczysc(self):
        """Czysci caly graf."""
        self.wierzcholki = []
        self.krawedzie = []
        self.lista_sasiedztwa = {}

    def zaladuj_przyklad(self):
        """Przykladowy graf do prezentacji na zajeciach."""
        self.wyczysc()
        przyklad = [
            ("A", "B", 4),
            ("A", "C", 2),
            ("B", "C", 1),
            ("B", "D", 5),
            ("C", "D", 8),
            ("C", "E", 10),
            ("D", "E", 2),
        ]
        for a, b, w in przyklad:
            self.dodaj_krawedz(a, b, w)
