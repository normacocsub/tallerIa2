import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog, QVBoxLayout, QLabel, QGroupBox, QWidget, QFrame
#import pyqtgraph as pg

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.initUI()
        
    def initUI(self):
        self.setGeometry(0, 200, 800, 800)
        self.setWindowTitle('PyQt5 Example')
        
        


        button = QPushButton('Cargar archivo', self)
        button.setStyleSheet('QPushButton {background-color: red; border: 1px solid black; color: white; min-width: 150px; border-radius: 5px; min-height: 40px; font-size: 18px; font-weight: bold;}')
        button.setToolTip('This is a button')
        button.move(100, 70)
        button.clicked.connect(self.on_button_file_click)



        self.file_information()  
        self.horizontal_line()     
        

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

    def horizontal_line(self):
        widget = QWidget(self)
        vbox = QVBoxLayout(widget)
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)  # Establecer la forma de la línea como horizontal
        vbox.addWidget(line)
        widget.setGeometry(0, 120, 800, 205)
        

    def on_button_file_click(self):
        filename, _ = QFileDialog.getOpenFileName(None, "Seleccionar archivo", ".", "Archivos TXT (*.txt);;Archivos CSV (*.csv)")
        if filename:
            print(filename)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('fusion') # aplicar el estilo "Fusion"
    window = Window()
    sys.exit(app.exec_())


#pip i pyqtgraph