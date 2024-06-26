import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def handle_graph(self, e):
        self._view.txt_result.clean()
        self._model.buildGraph()
        self._view.txt_result.controls.append(ft.Text(f'Numero di nodi : {self._model.numNodes()}'))
        self._view.txt_result.controls.append(ft.Text(f'Numero di archi : {self._model.numEdges()}'))
        self._view.txt_result.controls.append(ft.Text(f'Peso arco minore : {self._model.weightInfo()[0]} '
                                                      f'peso arco maggiore : {self._model.weightInfo()[1]}'))

        self._view.btn_countedges.disabled = False
        self._view.btn_search.disabled = False
        self._view.update_page()
    def handle_countedges(self, e):
        self._view.txt_result2.clean()
        l = self._view.txt_name.value
        try:
            lInt = int(self._view.txt_name.value)
        except Exception:
            self._view.txt_result2.controls.append(ft.Text("Inserire la soglia nel formato corretto"))
            self._view.update_page()
            return
        more,less = self._model.countLimit(lInt)
        self._view.txt_result2.controls.append(ft.Text(f'Numero archi con peso maggiore : {more}'))
        self._view.txt_result2.controls.append(ft.Text(f'Numero archi con peso minore : {less}'))

        self._view.update_page()


    def handle_search(self, e):
        self._view.txt_result3.clean()
        l = self._view.txt_name.value
        try:
            lInt = int(self._view.txt_name.value)
        except Exception:
            self._view.txt_result3.controls.append(ft.Text("Inserire la soglia nel formato corretto"))
            self._view.update_page()
            return
