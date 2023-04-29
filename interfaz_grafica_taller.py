import sys
from PyQt5.QtGui import QDoubleValidator
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLineEdit, QFileDialog, QVBoxLayout, QHBoxLayout, QLabel, QGroupBox, QWidget, QFrame, QComboBox
import plotly.graph_objs as go
import plotly.io as pio
import os
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl

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

        button = QPushButton('Iniciar red', self)
        button.setStyleSheet('QPushButton {background-color: red; border: 1px solid black; color: white; min-width: 150px; border-radius: 5px; min-height: 40px; font-size: 18px; font-weight: bold;}')
        button.setToolTip('This is a button')
        button.move(600, 895)

        button = QPushButton('Entrenar', self)
        button.setStyleSheet('QPushButton {background-color: red; border: 1px solid black; color: white; min-width: 150px; border-radius: 5px; min-height: 40px; font-size: 18px; font-weight: bold;}')
        button.setToolTip('This is a button')
        button.move(400, 895)

        button = QPushButton('Simular', self)
        button.setStyleSheet('QPushButton {background-color: red; border: 1px solid black; color: white; min-width: 150px; border-radius: 5px; min-height: 40px; font-size: 18px; font-weight: bold;}')
        button.setToolTip('This is a button')
        button.move(200, 895)

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
        group_box_layout.addWidget(QLabel("Total: 1"))
        group_box_layout.addWidget(QLabel("Entradas: 2"))
        group_box_layout.addWidget(QLabel("Salidas: 3"))

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
        fig = go.Figure(data=[go.Scatter(x=['A', 'B', 'C'], y=[1, 3, 2])])
        fig_html = pio.to_html(fig, full_html=False)

        graph_widget = QWebEngineView()
        graph_widget.setHtml(fig_html)

        main_widget = QWidget(self)
        main_layout = QVBoxLayout(main_widget)
        main_layout.addWidget(graph_widget)
        main_widget.setLayout(main_layout)
        main_widget.setGeometry(120, 510, 565, 340)

        ruta_figura = os.path.abspath("temp-plot.html")
        with open(ruta_figura, 'w', encoding='utf-8') as f:
            f.write(fig_html)

        
        graph_widget.load(QUrl.fromLocalFile(ruta_figura))

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
            print(filename)


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
