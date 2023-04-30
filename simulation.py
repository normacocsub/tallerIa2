from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import pyqtSlot

class Simulation(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        

        
        # Crear un diseño vertical para la vista secundaria
        layout = QVBoxLayout()
        
        # Crear una etiqueta de texto
        self.etiqueta = QLabel("Esta es la vista 2")
        
        # Agregar la etiqueta al diseño
        layout.addWidget(self.etiqueta)
        # Establecer el diseño para la vista secundaria
        self.setLayout(layout)

    @pyqtSlot(list)
    def actualizar_salidas(self, salidas):
        self.parent.salidas = salidas
        print(self.parent.salidas)