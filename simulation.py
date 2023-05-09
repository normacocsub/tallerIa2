from PyQt5.QtWidgets import QWidget, QVBoxLayout, QFileDialog, QLabel, QPushButton, QTableWidgetItem, QGroupBox, QTableWidget, QScrollArea
from PyQt5.QtCore import pyqtSlot, QUrl
import plotly.graph_objs as go
import plotly.io as pio
import os
import numpy as np
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile


class Simulation(QWidget):
    def __init__(self, parent ):
        super().__init__(parent )
        self.parent = parent

        titulo_style = """
            color: black;
            font-family: Arial;
            font-size: 24px;
            font-weight: bold;
            min-width: 300px;
        """
        self.parent.tipo_red = "Perceptron"
        self.total_patrones = 0
        self.total_entradas = 0
        self.entradas_vector = []
        self.salidas_vector = []
        self.patrones = []
        self.pesos = []
        self.umbrales = []
        self.isActivePesos = False
        self.isActiveUmbral = False
        self.isActivePatrones = False
        self.salidas_red = []
        
        # Crear un diseño vertical para la vista secundaria
        layout = QVBoxLayout()
        
        
        titulo = QLabel("Simulacion", self)
        titulo.setStyleSheet(titulo_style)
        titulo.move(300, 30)
        self.titulo = titulo

        self.buttons_file()
        self.file_information()
        self.table()
        self.grafica_entrenamiento()
        #al cargar el archivo deberia tomar este style
        self.style_green = 'QPushButton {background-color: green; border: 1px solid black; color: white; min-width: 150px; border-radius: 5px; min-height: 40px; font-size: 18px; font-weight: bold;}'
        
        # Establecer el diseño para la vista secundaria
        self.setLayout(layout)
    
    def grafica_entrenamiento(self):
        ruta_figura = os.path.abspath("temp-plot2.html")
        fig = go.Figure(data=[go.Scatter(x=[], y=[])])
        fig_html = pio.to_html(fig, full_html=False)
        graph_widget = QWebEngineView()
        profile = QWebEngineProfile.defaultProfile()
        profile.setHttpCacheType(QWebEngineProfile.NoCache)

        graph_widget.setHtml(fig_html)
        graph_widget.setFixedSize(600, 300)
        main_widget = QWidget(self)
        main_layout = QVBoxLayout(main_widget)
        main_layout.addWidget(graph_widget)
        main_widget.setLayout(main_layout)
        main_widget.setGeometry(90, 600, 600, 240)

        
        with open(ruta_figura, 'w', encoding='utf-8') as f:
            f.write(fig_html)

        
        graph_widget.load(QUrl.fromLocalFile(ruta_figura))
        self.graph_widget = graph_widget
    def update_grafica_entrenamiento(self):
        x_grafic = list(range(1, len(self.entradas_vector)+1))
        x2_grafic = list(range(1, self.total_entradas+1))
        fig = go.Figure(data=[go.Scatter(x=x_grafic, y=self.salidas_vector)])
        fig.add_trace(go.Scatter(x=x2_grafic, y=self.salidas_red))

        fig_html = pio.to_html(fig, full_html=False)

        # Guardar HTML en archivo temporal
        ruta_figura = os.path.abspath("temp-plot2.html")
        with open(ruta_figura, 'w', encoding='utf-8') as f:
            f.write(fig_html)

        # Cargar HTML en la instancia de QWebEngineView
        self.graph_widget.load(QUrl.fromLocalFile(ruta_figura))
    
    def file_information(self):
        # Crear un widget contenedor
        widget = QWidget(self)

        # Crear una disposición vertical dentro del widget contenedor
        vbox = QVBoxLayout(widget)
        # Crear un QGroupBox que contendrá las tres etiquetas

        group_box = QGroupBox("Información")
        group_box.setStyleSheet('QGroupBox { font-weight: bold; border: 2px solid gray; border-radius: 5px; padding-top: 10px; font-size: 15px; font-weight: bold; }')
        vbox.addWidget(group_box)

        # Crear tres etiquetas y agregarlas al QGroupBox
        group_box_layout = QVBoxLayout(group_box)
        group_box_layout.addWidget(QLabel(f"Patrones: {self.total_patrones}"))
        group_box_layout.addWidget(QLabel(f"Entradas: {self.total_entradas}"))
        self.group_box_layout = group_box_layout
        # Establecer el layout del widget contenedor
        widget.setLayout(vbox)
        widget.setGeometry(90, 180, 200, 150)

    def buttons_file(self):

        button = QPushButton('Regresar', self)
        button.setToolTip('This is a button')
        button.setStyleSheet('QPushButton { border: 1px solid black; background-color: blue; color: white; font-size: 14px; font-weight: bold; max-width: 40px;  }')
        button.move(20, 10)
        button.clicked.connect(self.regresar)
        self.button_pesos = button

        button = QPushButton('Cargar pesos', self)
        button.setToolTip('This is a button')
        button.move(100, 90)
        button.clicked.connect(self.cargar_pesos)
        self.button_pesos = button

        button = QPushButton('Cargar umbrales', self)
        button.setToolTip('This is a button')
        button.move(300, 90)
        button.clicked.connect(self.cargar_umbrales)
        self.button_umbrales = button

        button = QPushButton('Cargar patrones', self)
        button.setToolTip('This is a button')
        button.move(500, 90)
        button.clicked.connect(self.cargar_patrones)
        self.button_patrones = button

        button = QPushButton('Simular', self)
        button.setToolTip('This is a button')
        button.move(390, 230)
        button.setEnabled(False)
        button.setVisible(False)
        button.clicked.connect(self.simulate)
        self.button_simular = button

    def table(self):
        table_view = QTableWidget()
        table_view.setColumnCount(1)
        table_view.setRowCount(1)
        table_view.setItem(0, 0, QTableWidgetItem("Salidas"))
        table_view.setFixedSize(600, 250)
        table_view.setColumnWidth(0, 600)
        self.table_view = table_view
        scroll_area = QScrollArea(self)
        scroll_area.setWidget(table_view)
        scroll_area.setGeometry(100, 360, 600, 200)
        
    def cargar_pesos(self):
        filename, _ = QFileDialog.getOpenFileName(None, "Seleccionar archivo", ".", "Archivos TXT (*.txt);;Archivos CSV (*.csv)")
        if filename:
            self.button_pesos.setStyleSheet(self.style_green)
            if os.path.exists(filename):
                pesos = np.loadtxt(filename)
                if len(pesos.shape) == 1:
                    filas = len(pesos)
                    pesos = pesos.reshape((filas, 1))
                self.pesos = pesos
                self.isActivePesos = True
                self.activate_simulation_button()

    def cargar_umbrales(self):
        filename, _ = QFileDialog.getOpenFileName(None, "Seleccionar archivo", ".", "Archivos TXT (*.txt);;Archivos CSV (*.csv)")
        if filename:
            self.button_umbrales.setStyleSheet(self.style_green)
            if os.path.exists(filename):
                umbrales = np.atleast_1d(np.loadtxt(filename))
                self.umbrales = umbrales
                self.isActiveUmbral = True
                self.activate_simulation_button()

    def simulate(self):
        num_filas, salidas_total = self.parent.salidas.shape
        salidas = []
        for patron in range(self.total_patrones):
            salidas_neuronas = []
            for i in range(salidas_total):
                suma_entrada_pesos = 0
                # iteramos cada elemento del patron
                for j in range(self.total_entradas):
                    suma_entrada_pesos += ((self.patrones[patron][j] * self.pesos[j][i]))
                salida_neurona = suma_entrada_pesos - self.umbrales[i]
                if self.parent.tipo_red == "Perceptron":
                    if salida_neurona > 0:
                        salida_neurona = 1
                    else:
                        salida_neurona = 0
                salidas_neuronas.append(salida_neurona)
            salida =  " ".join(str(x) for x in salidas_neuronas)
            self.table_view.setItem((patron + 1), 0, QTableWidgetItem(salida))
            salidas.append(salida)
            self.salidas_red = salidas
        self.update_grafica_entrenamiento()

    def activate_simulation_button(self):
        if self.isActivePesos and self.isActiveUmbral and self.isActivePatrones:
            self.button_simular.setVisible(True)
            self.button_simular.setEnabled(True)
    def regresar(self):
        self.parent.stacked_widget.setCurrentIndex(0)
    def cargar_patrones(self):
        filename, _ = QFileDialog.getOpenFileName(None, "Seleccionar archivo", ".", "Archivos TXT (*.txt);;Archivos CSV (*.csv)")
        if filename:
            self.button_patrones.setStyleSheet(self.style_green)
            with open(filename) as f:
                lines = f.readlines()
            lines = [l.strip().split(';') for l in lines]
            data = lines[1:]

            matrix_entrada = [[float(x) for x in row[0:]] for row in data]
            matrix_entrada_np = np.array(matrix_entrada)
            
            num_filas, entradas_total = matrix_entrada_np.shape
            self.total_patrones = num_filas
            self.total_entradas = entradas_total
            self.patrones = matrix_entrada_np
            self.table_view.setRowCount(num_filas + 1)
            self.group_box_layout.itemAt(0).widget().setText(f"Patrones: {num_filas}")
            self.group_box_layout.itemAt(1).widget().setText(f"Entradas: {entradas_total}")
            self.isActivePatrones = True
            self.activate_simulation_button()

    
    @pyqtSlot(list)
    def actualizar_salidas(self, salidas):
        self.parent.salidas = np.array(salidas)
        self.salidas_vector = [" ".join(map(str, fila)) for fila in self.parent.salidas]
        print(self.salidas_vector)
    @pyqtSlot(list)
    def actualizar_entradas(self, entradas):
        self.parent.entradas = np.array(entradas)
        self.entradas_vector =  [" ".join(map(str, fila)) for fila in self.parent.entradas]
    @pyqtSlot(str)
    def actualizar_tipo_red(self, tipo_red):
        self.parent.tipo_red = tipo_red
    