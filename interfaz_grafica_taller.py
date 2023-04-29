import sys
from PyQt5.QtGui import QDoubleValidator
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLineEdit, QFileDialog, QVBoxLayout, QHBoxLayout, QLabel, QGroupBox, QWidget, QFrame, QComboBox
import plotly.graph_objs as go
import plotly.io as pio
import os
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile
from PyQt5.QtCore import QUrl
import numpy as np

class PositiveDoubleValidator(QDoubleValidator):
    def validate(self, input_str, pos):
        try:
            if input_str == "":
                state, input_str, pos = super().validate(input_str, pos)
                return state, input_str, pos
            if input_str == ".":
                return QDoubleValidator.Invalid, input_str, pos
            state, input_str, pos = super().validate(input_str, pos)
            if float(input_str) < 0:
                return QDoubleValidator.Invalid, input_str, pos
            return state, input_str, pos
        except:
            return QDoubleValidator.Invalid, input_str, pos


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.initUI()
        
    def initUI(self):
        
        self.setGeometry(0, 220, 800, 950)
        self.setFixedSize(800, 950)
        self.setWindowTitle('Entrenamiento red neuronal')
        self.error_iteration = [1, 3, 2]
        self.total_patrones = 0
        self.total_entradas = 0
        self.total_salidas = 0
        self.matriz_entradas = []
        self.matriz_salidas = []
        


        button = QPushButton('Cargar archivo', self)
        button.setStyleSheet('QPushButton {background-color: red; border: 1px solid black; color: white; min-width: 150px; border-radius: 5px; min-height: 40px; font-size: 18px; font-weight: bold;}')
        button.setToolTip('This is a button')
        button.move(100, 70)
        button.clicked.connect(self.on_button_file_click)



        self.file_information()  
        self.horizontal_line(1)     
        self.dropbox_tipo_red()
        self.textbox_iterations()
        self.texbox_max_error()
        self.texbox_rata_aprendizaje()
        self.horizontal_line(2)  
        self.grafica_entrenamiento()

        button_red = QPushButton('Iniciar red', self)
        button_red.setToolTip('This is a button')
        button_red.move(550, 895)
        self.button_iniciar_red = button_red

        button_entrenar = QPushButton('Entrenar', self)
        button_entrenar.setToolTip('This is a button')
        button_entrenar.move(350, 895)
        button_entrenar.setEnabled(False)
        self.button_entrenar = button_entrenar

        button_simular = QPushButton('Simular', self)
        button_simular.setToolTip('This is a button')
        button_simular.move(150, 895)
        button_simular.setEnabled(False)
        self.button_simular = button_simular

        self.show()

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
        group_box_layout.addWidget(QLabel(f"Salidas: {self.total_salidas}"))
        self.group_box_layout = group_box_layout
        # Establecer el layout del widget contenedor
        widget.setLayout(vbox)
        widget.setGeometry(400, 40, 200, 150)

    def dropbox_tipo_red(self):
        central_widget = QWidget(self)

        # Crear un layout vertical
        vbox = QVBoxLayout(central_widget)

        # Crear un layout horizontal
        hbox = QHBoxLayout()

        # Agregar un label al layout horizontal
        label = QLabel("Tipo de red:")
        hbox.addWidget(label)

        # Agregar un combo box al layout horizontal
        combo_box = QComboBox()
        combo_box.addItem("Perceptron")
        combo_box.addItem("Adaline")

        hbox.addWidget(combo_box)

        # Agregar el layout horizontal al layout vertical
        vbox.addLayout(hbox)

        central_widget.setLayout(vbox)
        central_widget.setGeometry(80, 200, 250, 200)
    
    def textbox_iterations(self):
        widget = QWidget(self)

        # Crear un layout vertical
        vbox = QVBoxLayout(widget)

        # Crear un layout horizontal
        hbox = QHBoxLayout()

        label = QLabel("Iteraciones:")
        hbox.addWidget(label)

        text_box = QLineEdit()
        text_box.setValidator(PositiveDoubleValidator())
        hbox.addWidget(text_box)
        vbox.addLayout(hbox)
        widget.setLayout(vbox)
        widget.setGeometry(420, 200, 250, 200)

    def texbox_max_error(self):
        widget = QWidget(self)

        # Crear un layout vertical
        vbox = QVBoxLayout(widget)

        # Crear un layout horizontal
        hbox = QHBoxLayout()

        label = QLabel("Error maximo:")
        hbox.addWidget(label)

        text_box = QLineEdit()
        text_box.setValidator(PositiveDoubleValidator())
        hbox.addWidget(text_box)
        vbox.addLayout(hbox)
        widget.setLayout(vbox)
        widget.setGeometry(65, 300, 265, 200)
    
    def texbox_rata_aprendizaje(self):
        widget = QWidget(self)

        # Crear un layout vertical
        vbox = QVBoxLayout(widget)

        # Crear un layout horizontal
        hbox = QHBoxLayout()

        label = QLabel("Rata aprendizaje:")
        hbox.addWidget(label)

        text_box = QLineEdit()
        text_box.setValidator(PositiveDoubleValidator())
        hbox.addWidget(text_box)
        vbox.addLayout(hbox)
        widget.setLayout(vbox)
        widget.setGeometry(383, 300, 285, 200)
       
    def grafica_entrenamiento(self):
        ruta_figura = os.path.abspath("temp-plot.html")
        fig = go.Figure(data=[go.Scatter(x=['A', 'B', 'C'], y=self.error_iteration)])
        fig_html = pio.to_html(fig, full_html=False)
        graph_widget = QWebEngineView()

        profile = QWebEngineProfile.defaultProfile()
        profile.setHttpCacheType(QWebEngineProfile.NoCache)

        graph_widget.setHtml(fig_html)

        main_widget = QWidget(self)
        main_layout = QVBoxLayout(main_widget)
        main_layout.addWidget(graph_widget)
        main_widget.setLayout(main_layout)
        main_widget.setGeometry(120, 510, 565, 340)

        
        with open(ruta_figura, 'w', encoding='utf-8') as f:
            f.write(fig_html)

        
        graph_widget.load(QUrl.fromLocalFile(ruta_figura))
        self.graph_widget = graph_widget

    def update_grafica_entrenamiento(self):
        fig = go.Figure(data=[go.Scatter(x=['A', 'B', 'C'], y=self.error_iteration)])
        fig_html = pio.to_html(fig, full_html=False)

        # Guardar HTML en archivo temporal
        ruta_figura = os.path.abspath("temp-plot.html")
        with open(ruta_figura, 'w', encoding='utf-8') as f:
            f.write(fig_html)

        # Cargar HTML en la instancia de QWebEngineView
        self.graph_widget.load(QUrl.fromLocalFile(ruta_figura))

    def horizontal_line(self, val):
        widget = QWidget(self)
        vbox = QVBoxLayout(widget)
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)  # Establecer la forma de la línea como horizontal
        vbox.addWidget(line)
        widget.setGeometry(0, 120 if val == 1 else 400, 800, 205)
        

    def on_button_file_click(self):
        filename, _ = QFileDialog.getOpenFileName(None, "Seleccionar archivo", ".", "Archivos TXT (*.txt);;Archivos CSV (*.csv)")
        if filename:
            with open(filename) as f:
                lines = f.readlines()

            # Elimina los caracteres de nueva línea y divide las líneas en columnas usando ';'
            lines = [l.strip().split(';') for l in lines]

            # Separa la primera fila del resto de las filas
            header = lines[0]
            data = lines[1:]

            # Convierte la primera fila en un vector
            header_vector = [str(x) for x in header[0:]]

            s1_index = header_vector.index('s1')

            # Convierte las filas restantes en una matriz
            matrix_entrada = [[int(x) for x in row[0:s1_index]] for row in data]
            matrix_entrada_np = np.array(matrix_entrada)
            num_filas, entradas_total = matrix_entrada_np.shape

            matrix_salida = [[int(x) for x in row[s1_index:]] for row in data]
            matrix_salida_np = np.array(matrix_salida)
            num_filas, salidas_total = matrix_salida_np.shape

            #actualizamos variables
            self.total_patrones = num_filas
            self.total_entradas = entradas_total
            self.total_salidas = salidas_total
            self.matriz_entradas = matrix_entrada_np
            self.matriz_salidas= matrix_salida_np

            #actualizamos labels
            self.group_box_layout.itemAt(0).widget().setText(f"Patrones: {num_filas}")
            self.group_box_layout.itemAt(1).widget().setText(f"Entradas: {entradas_total}")
            self.group_box_layout.itemAt(2).widget().setText(f"Salidas: {salidas_total}")

            #prueba actualizando grafica / se debe remover proximente
            self.error_iteration = [2,3,8]
            self.update_grafica_entrenamiento()
            self.graph_widget.reload()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('fusion') # aplicar el estilo "Fusion"
    with open('styles.qss', 'r') as f:
        stylesheet = f.read()
        app.setStyleSheet(stylesheet)
    window = Window()
    sys.exit(app.exec_())


#pip i pyqtgraph
#pip install PyQtWebEngine
