from datetime import datetime

import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._choiceAeroportoP = None
        self._choiceAeroportoA = None
        self._view = view
        # the modello, which implements the logic of the program and holds the data
        self._model = model

    def handleAnalizza(self, e):
        try:
            nMin = int(self._view._txtInNumC.value)
        except ValueError:
            self._view.create_alert("Inserisci un numero!!")
            return
        self._model.buildGraph(nMin)

        self._view.txt_result.controls.append(ft.Text("Grafo correttamente creato.", color="green"))
        self._view.txt_result.controls.append(ft.Text(f"Numero di nodi: {self._model.getNumNodi()}"))
        self._view.txt_result.controls.append(ft.Text(f"Numero di archi: {self._model.getNumArchi()}"))

        self._view._ddAeroportoP.disabled = False
        self._view._ddAeroportoA.disabled = False
        self._view._btnConnessi.disabled = False
        self._view._btnPercorsoTrovato.disabled = False
        self.fillDD()
        self._view.update_page()

    def handleConnessi(self, e):
        if self._choiceAeroportoP is None:
            self._view.create_alert("Selezionare un aeroporto!")
            return
        v0 = self._choiceAeroportoP
        if v0 is None:
            self._view.create_alert("Il nodo non è presente nel grafo!")
            return
        vicini = self._model.getSortedVicini(v0)
        self._view.txt_result.controls.append(ft.Text(f"Ecco i vicini di {v0}"))
        for v in vicini:
            self._view.txt_result.controls.append(ft.Text(f"{v[1]} - {v[0]}"))
        self._view.update_page()

    def handleTestConnessione(self, e):
        self._view.txt_result.controls.clear()
        v0 = self._choiceAeroportoP
        v1 = self._choiceAeroportoA

        if v0 is None or v1 is None:
            self._view.create_alert("Selezionare degli aeroporti tra cui poter calcolare un percorso!!")
            return

        # Verificare che ci sia un percorso
        if not self._model.esistePercorso(v0, v1):
            self._view.txt_result.controls.append(ft.Text(f"Non esiste un percorso tra {v0} e {v1}", color="red"))
        else:
            self._view.txt_result.controls.append(
                ft.Text(f"E' stato trovato un percorso tra {v0} e {v1}", color="green"))

        # Trovare un possibile percorso
        path = self._model.trovaCamminoBFS(v0, v1)
        self._view.txt_result.controls.append(ft.Text(f"Il cammino con minor numero di archi {v0} e {v1} è: "))
        for p in path:
            self._view.txt_result.controls.append(ft.Text(f"{p}"))
        self._view._txtInNumTratte.disabled = False
        self._view._btnPercorso.disabled = False
        self._view.update_page()

    def handleCercaItinerario(self, e):
        print("called cercaItinerario")
        v0 = self._choiceAeroportoP
        v1 = self._choiceAeroportoA
        if v0 is None or v1 is None:
            self._view.create_alert("Selezionare degli aeroporti tra cui poter calcolare un percorso!!")
            return
        try:
            t = int(self._view._txtInNumTratte.value)


        except ValueError:
            self._view.create_alert("Il valore inserito non è un numero!")
            return
        tic = datetime.now()
        path, nTot = self._model.getCamminoOttimo(v0, v1, t)
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"Il percorso ottimo tra {v0} e {v1}:"))
        for p in path:
            self._view.txt_result.controls.append(ft.Text(p))
        self._view.txt_result.controls.append(
            ft.Text(f"Tempo impiegato per la ricerca: {datetime.now() - tic} secondi"))
        self._view.txt_result.controls.append(ft.Text(f"Numero totale di voli: {nTot}"))
        self._view.update_page()

    def fillDD(self):
        allNodes = self._model.getAllNodes()
        for n in allNodes:
            self._view._ddAeroportoP.options.append(ft.dropdown.Option(data=n,
                                                                       on_click=self.readDDAeroportoP,
                                                                       text=n.AIRPORT)
                                                    )

            self._view._ddAeroportoA.options.append(ft.dropdown.Option(data=n,
                                                                       on_click=self.readDDAeroportoA,
                                                                       text=n.AIRPORT)
                                                    )

    def readDDAeroportoP(self, e):
        if e.control.data is None:
            self._choiceAeroportoP = None
        else:
            self._choiceAeroportoP = e.control.data
        print(f"readdDDAeroporto called -- {self._choiceAeroportoP}")

    def readDDAeroportoA(self, e):
        if e.control.data is None:
            self._choiceAeroportoA = None
        else:
            self._choiceAeroportoA = e.control.data
        print(f"readdDDAeroporto called -- {self._choiceAeroportoA}")
