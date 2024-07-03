import flet as ft


class View(ft.UserControl):
    def __init__(self, page: ft.Page):
        super().__init__()
        # page stuff
        self._ddAeroportA = None
        self._ddAeroportoP = None
        self._page = page
        self._page.title = "Template application using MVC and DAO"
        self._page.horizontal_alignment = 'CENTER'
        self._page.theme_mode = ft.ThemeMode.LIGHT
        # controller (it is not initialized. Must be initialized in the main, after the controller is created)
        self._controller = None
        # graphical elements
        self._title = None
        self.txt_result = None

    def load_interface(self):
        # title
        self._title = ft.Text("TdP Flights Manager 2024", color="blue", size=24)
        self._page.controls.append(self._title)

        # Row 1
        self._txtInNumC = ft.TextField(label="Numero compagnie", width=250)
        self._btnAnalizza = ft.ElevatedButton(text="Analizza Aeroporti", on_click=self._controller.handleAnalizza)
        self._btnConnessi = ft.ElevatedButton(text="Aeroporti connessi", disabled=True, on_click=self._controller.handleConnessi)
        row1 = ft.Row([self._txtInNumC, self._btnAnalizza, self._btnConnessi],
                      alignment=ft.MainAxisAlignment.CENTER)
        self._page.controls.append(row1)

        # Row 2
        self._ddAeroportoP = ft.Dropdown(label="Partenza", disabled=True, width=400)
        self._ddAeroportoA = ft.Dropdown(label="Arrivo", disabled=True, width=400)
        self._btnPercorsoTrovato = ft.ElevatedButton(text="Percorso", disabled=True, on_click=self._controller.handleTestConnessione)
        row2 = ft.Row([self._ddAeroportoP, self._ddAeroportoA, self._btnPercorsoTrovato],
                      alignment=ft.MainAxisAlignment.CENTER)
        self._page.controls.append(row2)

        # Row 3
        self._txtInNumTratte = ft.TextField(label="Num Tratte max", width=250)
        self._btnPercorso = ft.ElevatedButton(text="Cerca itinerario",
                                              disabled=True,
                                              on_click=self._controller.handleCercaItinerario)
        row3 = ft.Row([self._txtInNumTratte, self._btnPercorso],
                      alignment=ft.MainAxisAlignment.CENTER)
        self._page.controls.append(row3)

        # List View where the reply is printed
        self.txt_result = ft.ListView(expand=1, spacing=10, padding=20, auto_scroll=False)
        self._page.controls.append(self.txt_result)
        self._page.update()

    @property
    def controller(self):
        return self._controller

    @controller.setter
    def controller(self, controller):
        self._controller = controller

    def set_controller(self, controller):
        self._controller = controller

    def create_alert(self, message):
        dlg = ft.AlertDialog(title=ft.Text(message))
        self._page.dialog = dlg
        dlg.open = True
        self._page.update()

    def update_page(self):
        self._page.update()
