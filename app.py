"""
Aplikacja graficzna - Algorytm Dijkstry
Autorzy: Patryk Abel, Aleksander Korsak
Studenci inżynierii cyberprzestrzeni, Uniwersytet Pomorski w Slupsku
"""

import tkinter as tk
from tkinter import ttk, messagebox
import math

from graf import Graf
from dijkstra import dijkstra


# kolory aplikacji - ciemny motyw wyglada lepiej na prezentacji
KOLOR_TLO = "#1a1a2e"
KOLOR_PANEL = "#16213e"
KOLOR_AKCENT = "#0f3460"
KOLOR_PRZYCISK = "#e94560"
KOLOR_TEKST = "#eaeaea"
KOLOR_WIERZCHOLEK = "#53d8fb"
KOLOR_START = "#4ecca3"
KOLOR_KONIEC = "#e94560"
KOLOR_SCIEZKA = "#ffd369"


class AplikacjaDijkstra:
    def __init__(self, root):
        self.root = root
        self.root.title("Algorytm Dijkstry - projekt")
        self.root.geometry("1100x700")
        self.root.configure(bg=KOLOR_TLO)
        self.root.minsize(900, 600)

        self.graf = Graf()
        self.start = None
        self.koniec = None
        self.ostatnia_sciezka = []

        self._stworz_interfejs()
        self.graf.zaladuj_przyklad()
        self.start = "A"
        self.koniec = "E"
        self._odswiez_wszystko()

    def _stworz_interfejs(self):
        # naglowek z autorami
        naglowek = tk.Frame(self.root, bg=KOLOR_AKCENT, pady=10)
        naglowek.pack(fill=tk.X)

        tk.Label(
            naglowek,
            text="Algorytm Dijkstry",
            font=("Segoe UI", 18, "bold"),
            bg=KOLOR_AKCENT,
            fg=KOLOR_TEKST,
        ).pack()

        tk.Label(
            naglowek,
            text="Patryk Abel  |  Aleksander Korsak",
            font=("Segoe UI", 10),
            bg=KOLOR_AKCENT,
            fg="#a0a0a0",
        ).pack()

        # glowny kontener
        glowny = tk.Frame(self.root, bg=KOLOR_TLO)
        glowny.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # lewy panel - sterowanie
        lewy = tk.Frame(glowny, bg=KOLOR_PANEL, width=320)
        lewy.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        lewy.pack_propagate(False)

        self._panel_dodawania(lewy)
        self._panel_wyboru(lewy)
        self._panel_wyniku(lewy)

        # prawy panel - wizualizacja i reprezentacja grafu
        prawy = tk.Frame(glowny, bg=KOLOR_TLO)
        prawy.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self._panel_wizualizacji(prawy)
        self._panel_reprezentacji(prawy)

    def _panel_dodawania(self, parent):
        ramka = tk.LabelFrame(
            parent, text=" Budowanie grafu ", font=("Segoe UI", 10, "bold"),
            bg=KOLOR_PANEL, fg=KOLOR_TEKST, padx=8, pady=8,
        )
        ramka.pack(fill=tk.X, padx=8, pady=8)

        # wierzcholek
        tk.Label(ramka, text="Wierzcholek:", bg=KOLOR_PANEL, fg=KOLOR_TEKST).grid(row=0, column=0, sticky="w")
        self.entry_wierzcholek = tk.Entry(ramka, width=8, font=("Consolas", 11))
        self.entry_wierzcholek.grid(row=0, column=1, padx=4)

        btn_w = tk.Button(
            ramka, text="+ Dodaj", command=self._dodaj_wierzcholek,
            bg=KOLOR_PRZYCISK, fg="white", font=("Segoe UI", 9), relief=tk.FLAT, cursor="hand2",
        )
        btn_w.grid(row=0, column=2, padx=4)

        # krawedz
        tk.Label(ramka, text="Krawedz:", bg=KOLOR_PANEL, fg=KOLOR_TEKST).grid(row=1, column=0, sticky="w", pady=(8, 0))
        krawedz_ramka = tk.Frame(ramka, bg=KOLOR_PANEL)
        krawedz_ramka.grid(row=1, column=1, columnspan=2, sticky="w", pady=(8, 0))
        self.entry_a = tk.Entry(krawedz_ramka, width=4, font=("Consolas", 11))
        self.entry_a.pack(side=tk.LEFT)
        tk.Label(krawedz_ramka, text=" — ", bg=KOLOR_PANEL, fg=KOLOR_TEKST).pack(side=tk.LEFT)
        self.entry_b = tk.Entry(krawedz_ramka, width=4, font=("Consolas", 11))
        self.entry_b.pack(side=tk.LEFT)

        tk.Label(ramka, text="Waga:", bg=KOLOR_PANEL, fg=KOLOR_TEKST).grid(row=2, column=0, sticky="w", pady=(4, 0))
        self.entry_waga = tk.Entry(ramka, width=8, font=("Consolas", 11))
        self.entry_waga.grid(row=2, column=1, padx=4, pady=(4, 0))

        btn_k = tk.Button(
            ramka, text="+ Dodaj krawedz", command=self._dodaj_krawedz,
            bg=KOLOR_PRZYCISK, fg="white", font=("Segoe UI", 9), relief=tk.FLAT, cursor="hand2",
        )
        btn_k.grid(row=2, column=2, padx=4, pady=(4, 0))

        # przyciski pomocnicze
        przyciski = tk.Frame(ramka, bg=KOLOR_PANEL)
        przyciski.grid(row=3, column=0, columnspan=3, pady=(10, 0))

        tk.Button(
            przyciski, text="Przyklad", command=self._wczytaj_przyklad,
            bg=KOLOR_AKCENT, fg=KOLOR_TEKST, font=("Segoe UI", 9), relief=tk.FLAT, cursor="hand2",
        ).pack(side=tk.LEFT, padx=2)

        tk.Button(
            przyciski, text="Wyczysc", command=self._wyczysc_graf,
            bg="#555", fg=KOLOR_TEKST, font=("Segoe UI", 9), relief=tk.FLAT, cursor="hand2",
        ).pack(side=tk.LEFT, padx=2)

    def _panel_wyboru(self, parent):
        ramka = tk.LabelFrame(
            parent, text=" Wybor wierzcholkow ", font=("Segoe UI", 10, "bold"),
            bg=KOLOR_PANEL, fg=KOLOR_TEKST, padx=8, pady=8,
        )
        ramka.pack(fill=tk.X, padx=8, pady=8)

        tk.Label(ramka, text="Start:", bg=KOLOR_PANEL, fg=KOLOR_START,
                 font=("Segoe UI", 10, "bold")).grid(row=0, column=0, sticky="w")
        self.combo_start = ttk.Combobox(ramka, width=10, state="readonly", font=("Consolas", 11))
        self.combo_start.grid(row=0, column=1, padx=4)

        tk.Label(ramka, text="Koniec:", bg=KOLOR_PANEL, fg=KOLOR_KONIEC,
                 font=("Segoe UI", 10, "bold")).grid(row=1, column=0, sticky="w", pady=(6, 0))
        self.combo_koniec = ttk.Combobox(ramka, width=10, state="readonly", font=("Consolas", 11))
        self.combo_koniec.grid(row=1, column=1, padx=4, pady=(6, 0))

        btn_szukaj = tk.Button(
            ramka, text="▶  Oblicz najkrotsza droge (Dijkstra)",
            command=self._oblicz_dijkstre,
            bg=KOLOR_START, fg="#1a1a2e", font=("Segoe UI", 10, "bold"),
            relief=tk.FLAT, cursor="hand2", pady=6,
        )
        btn_szukaj.grid(row=2, column=0, columnspan=2, pady=(12, 0), sticky="ew")

        tk.Label(
            ramka,
            text="Tip: kliknij wierzcholek na grafie\naby ustawic start lub koniec",
            bg=KOLOR_PANEL, fg="#888", font=("Segoe UI", 8), justify=tk.LEFT,
        ).grid(row=3, column=0, columnspan=2, pady=(8, 0))

        self.tryb_klikniecia = tk.StringVar(value="start")
        tryb_ramka = tk.Frame(ramka, bg=KOLOR_PANEL)
        tryb_ramka.grid(row=4, column=0, columnspan=2, pady=(4, 0))

        tk.Radiobutton(
            tryb_ramka, text="Klik = Start", variable=self.tryb_klikniecia, value="start",
            bg=KOLOR_PANEL, fg=KOLOR_START, selectcolor=KOLOR_AKCENT, activebackground=KOLOR_PANEL,
        ).pack(side=tk.LEFT)
        tk.Radiobutton(
            tryb_ramka, text="Klik = Koniec", variable=self.tryb_klikniecia, value="koniec",
            bg=KOLOR_PANEL, fg=KOLOR_KONIEC, selectcolor=KOLOR_AKCENT, activebackground=KOLOR_PANEL,
        ).pack(side=tk.LEFT, padx=8)

    def _panel_wyniku(self, parent):
        ramka = tk.LabelFrame(
            parent, text=" Wynik ", font=("Segoe UI", 10, "bold"),
            bg=KOLOR_PANEL, fg=KOLOR_TEKST, padx=8, pady=8,
        )
        ramka.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)

        self.label_dlugosc = tk.Label(
            ramka, text="Dlugosc: —", bg=KOLOR_PANEL, fg=KOLOR_SCIEZKA,
            font=("Segoe UI", 12, "bold"), anchor="w",
        )
        self.label_dlugosc.pack(fill=tk.X)

        self.label_sciezka = tk.Label(
            ramka, text="Sciezka: —", bg=KOLOR_PANEL, fg=KOLOR_TEKST,
            font=("Consolas", 11), anchor="w", wraplength=280, justify=tk.LEFT,
        )
        self.label_sciezka.pack(fill=tk.X, pady=(6, 0))

    def _panel_wizualizacji(self, parent):
        ramka = tk.LabelFrame(
            parent, text=" Wizualizacja grafu ", font=("Segoe UI", 10, "bold"),
            bg=KOLOR_PANEL, fg=KOLOR_TEKST,
        )
        ramka.pack(fill=tk.BOTH, expand=True, pady=(0, 8))

        self.canvas = tk.Canvas(ramka, bg="#0d1117", highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=4, pady=4)
        self.canvas.bind("<Configure>", lambda e: self._rysuj_graf())
        self.canvas.bind("<Button-1>", self._klikniecie_canvas)

        self.pozycje = {}  # gdzie sa narysowane wierzcholki

    def _panel_reprezentacji(self, parent):
        ramka = tk.LabelFrame(
            parent, text=" Reprezentacja grafu ", font=("Segoe UI", 10, "bold"),
            bg=KOLOR_PANEL, fg=KOLOR_TEKST,
        )
        ramka.pack(fill=tk.BOTH)

        self.notebook = ttk.Notebook(ramka)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=4, pady=4)

        # zakladka lista sasiedztwa
        fr_lista = tk.Frame(self.notebook, bg="#0d1117")
        self.notebook.add(fr_lista, text="  Lista sasiedztwa  ")

        self.text_lista = tk.Text(
            fr_lista, bg="#0d1117", fg="#7ee787", font=("Consolas", 11),
            relief=tk.FLAT, padx=10, pady=10, height=8,
        )
        self.text_lista.pack(fill=tk.BOTH, expand=True)
        self.text_lista.config(state=tk.DISABLED)

        # zakladka macierz sasiedztwa
        fr_macierz = tk.Frame(self.notebook, bg="#0d1117")
        self.notebook.add(fr_macierz, text="  Macierz sasiedztwa  ")

        self.text_macierz = tk.Text(
            fr_macierz, bg="#0d1117", fg="#79c0ff", font=("Consolas", 11),
            relief=tk.FLAT, padx=10, pady=10, height=8,
        )
        self.text_macierz.pack(fill=tk.BOTH, expand=True)
        self.text_macierz.config(state=tk.DISABLED)

    # --- akcje uzytkownika ---

    def _dodaj_wierzcholek(self):
        nazwa = self.entry_wierzcholek.get().strip()
        if not nazwa:
            messagebox.showwarning("Uwaga", "Podaj nazwe wierzcholka!")
            return
        self.graf.dodaj_wierzcholek(nazwa)
        self.entry_wierzcholek.delete(0, tk.END)
        self._odswiez_wszystko()

    def _dodaj_krawedz(self):
        a = self.entry_a.get().strip()
        b = self.entry_b.get().strip()
        waga = self.entry_waga.get().strip()

        if not a or not b or not waga:
            messagebox.showwarning("Uwaga", "Uzupelnij oba wierzcholki i wage!")
            return
        try:
            float(waga)
        except ValueError:
            messagebox.showwarning("Uwaga", "Waga musi byc liczba!")
            return

        if a == b:
            messagebox.showwarning("Uwaga", "Wierzcholki musza byc rozne!")
            return

        self.graf.dodaj_krawedz(a, b, waga)
        self.entry_a.delete(0, tk.END)
        self.entry_b.delete(0, tk.END)
        self.entry_waga.delete(0, tk.END)
        self._odswiez_wszystko()

    def _wczytaj_przyklad(self):
        self.graf.zaladuj_przyklad()
        self.start = "A"
        self.koniec = "E"
        self.ostatnia_sciezka = []
        self._odswiez_wszystko()

    def _wyczysc_graf(self):
        if messagebox.askyesno("Potwierdzenie", "Na pewno wyczyscic graf?"):
            self.graf.wyczysc()
            self.start = None
            self.koniec = None
            self.ostatnia_sciezka = []
            self._odswiez_wszystko()

    def _oblicz_dijkstre(self):
        self.start = self.combo_start.get() or self.start
        self.koniec = self.combo_koniec.get() or self.koniec

        if not self.start or not self.koniec:
            messagebox.showwarning("Uwaga", "Wybierz wierzcholek startowy i docelowy!")
            return

        if self.start not in self.graf.wierzcholki or self.koniec not in self.graf.wierzcholki:
            messagebox.showwarning("Uwaga", "Wybrane wierzcholki nie istnieja w grafie!")
            return

        dlugosc, sciezka = dijkstra(self.graf.lista_sasiedztwa, self.start, self.koniec)

        if dlugosc is None:
            self.ostatnia_sciezka = []
            self.label_dlugosc.config(text="Dlugosc: brak drogi")
            self.label_sciezka.config(text="Sciezka: —")
            messagebox.showinfo("Wynik", f"Nie ma drogi z {self.start} do {self.koniec}")
        else:
            self.ostatnia_sciezka = sciezka
            self.label_dlugosc.config(text=f"Dlugosc: {dlugosc}")
            self.label_sciezka.config(text=f"Sciezka: {' → '.join(sciezka)}")

        self._rysuj_graf()

    def _klikniecie_canvas(self, event):
        """Klikniecie w wierzcholek na canvasie ustawia start lub koniec."""
        for nazwa, (x, y) in self.pozycje.items():
            if (event.x - x) ** 2 + (event.y - y) ** 2 <= 20 ** 2:
                if self.tryb_klikniecia.get() == "start":
                    self.start = nazwa
                    self.combo_start.set(nazwa)
                else:
                    self.koniec = nazwa
                    self.combo_koniec.set(nazwa)
                self._rysuj_graf()
                return

    def _odswiez_wszystko(self):
        """Odswieza comboboxy, teksty i rysunek."""
        wierzcholki = self.graf.wierzcholki
        self.combo_start["values"] = wierzcholki
        self.combo_koniec["values"] = wierzcholki

        if self.start and self.start in wierzcholki:
            self.combo_start.set(self.start)
        elif wierzcholki:
            self.combo_start.set(wierzcholki[0])

        if self.koniec and self.koniec in wierzcholki:
            self.combo_koniec.set(self.koniec)
        elif len(wierzcholki) > 1:
            self.combo_koniec.set(wierzcholki[-1])

        self._aktualizuj_tekst(self.text_lista, self.graf.tekst_listy())
        self._aktualizuj_tekst(self.text_macierz, self.graf.tekst_macierzy())
        self._rysuj_graf()

    def _aktualizuj_tekst(self, widget, tekst):
        widget.config(state=tk.NORMAL)
        widget.delete("1.0", tk.END)
        widget.insert("1.0", tekst)
        widget.config(state=tk.DISABLED)

    def _rysuj_graf(self):
        """Rysuje graf na canvasie - wierzcholki w kole, krawedzie z wagami."""
        self.canvas.delete("all")
        self.pozycje = {}

        wierzcholki = self.graf.wierzcholki
        if not wierzcholki:
            self.canvas.create_text(
                self.canvas.winfo_width() // 2, self.canvas.winfo_height() // 2,
                text="Dodaj wierzcholki i krawedzie", fill="#555", font=("Segoe UI", 14),
            )
            return

        cx = self.canvas.winfo_width() // 2
        cy = self.canvas.winfo_height() // 2
        promien = min(cx, cy) - 60
        n = len(wierzcholki)

        # pozycje wierzcholkow na okregu
        for i, w in enumerate(wierzcholki):
            kat = 2 * math.pi * i / n - math.pi / 2
            x = cx + promien * math.cos(kat)
            y = cy + promien * math.sin(kat)
            self.pozycje[w] = (x, y)

        sciezka_krawedzi = set()
        for j in range(len(self.ostatnia_sciezka) - 1):
            a, b = self.ostatnia_sciezka[j], self.ostatnia_sciezka[j + 1]
            sciezka_krawedzi.add(tuple(sorted([a, b])))

        # krawedzie
        for a, b, waga in self.graf.krawedzie:
            x1, y1 = self.pozycje[a]
            x2, y2 = self.pozycje[b]
            na_sciezce = tuple(sorted([a, b])) in sciezka_krawedzi
            kolor = KOLOR_SCIEZKA if na_sciezce else "#444"
            szer = 3 if na_sciezce else 1

            self.canvas.create_line(x1, y1, x2, y2, fill=kolor, width=szer)

            # waga na srodku krawedzi
            mx, my = (x1 + x2) / 2, (y1 + y2) / 2
            self.canvas.create_rectangle(mx - 14, my - 10, mx + 14, my + 10, fill="#0d1117", outline="")
            self.canvas.create_text(mx, my, text=str(int(waga) if waga == int(waga) else waga),
                                    fill=KOLOR_SCIEZKA if na_sciezce else "#aaa", font=("Consolas", 9, "bold"))

        # wierzcholki
        for w, (x, y) in self.pozycje.items():
            if w == self.start:
                kolor = KOLOR_START
            elif w == self.koniec:
                kolor = KOLOR_KONIEC
            elif w in self.ostatnia_sciezka:
                kolor = KOLOR_SCIEZKA
            else:
                kolor = KOLOR_WIERZCHOLEK

            self.canvas.create_oval(x - 22, y - 22, x + 22, y + 22, fill=kolor, outline="white", width=2)
            self.canvas.create_text(x, y, text=w, fill="#1a1a2e", font=("Segoe UI", 11, "bold"))


def main():
    root = tk.Tk()
    # styl dla comboboxow
    style = ttk.Style()
    style.theme_use("clam")
    AplikacjaDijkstra(root)
    root.mainloop()


if __name__ == "__main__":
    main()
