# pycalc.py
"""Una calculadora sencilla construida con Python y PyQt6."""

import sys
from functools import partial

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QGridLayout,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
)

# Constantes de la aplicación
ERROR_MSG = "ERROR"
WINDOW_SIZE = 235
DISPLAY_HEIGHT = 35
BUTTON_SIZE = 40

# --- EL MODELO (Lógica de Negocio) ---

def evaluateExpression(expression):
    """Evalúa una expresión matemática (Modelo)."""
    try:
        # Usa diccionarios vacíos para 'globals' y 'locals' por seguridad
        result = str(eval(expression, {}, {}))
    except Exception:
        result = ERROR_MSG
    return result


# --- LA VISTA (GUI) ---

class PyCalcWindow(QMainWindow):
    """La Vista (GUI) de la calculadora."""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyCalc")
        self.setFixedSize(WINDOW_SIZE, WINDOW_SIZE)
        
        # Configuración del widget central y el layout principal
        self.generalLayout = QVBoxLayout()
        self._centralWidget = QWidget(self)
        self.setCentralWidget(self._centralWidget)
        self._centralWidget.setLayout(self.generalLayout)
        
        # Crea la pantalla y los botones
        self._createDisplay()
        self._createButtons()

    def _createDisplay(self):
        """Crea el widget de visualización (QLineEdit)."""
        self.display = QLineEdit()
        self.display.setFixedSize(WINDOW_SIZE - 10, DISPLAY_HEIGHT)
        self.display.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.display.setReadOnly(True)
        
        # Añade la pantalla al layout general
        self.generalLayout.addWidget(self.display)

    def _createButtons(self):
        """Crea los botones del teclado de la calculadora."""
        self.buttonMap = {}
        buttonsLayout = QGridLayout()
        
        # Definición del teclado: [fila][columna]
        keyBoard = [
            ["7", "8", "9", "/", "C"],
            ["4", "5", "6", "*", "("],
            ["1", "2", "3", "-", ")"],
            ["0", "00", ".", "+", "="],
        ]
        
        # Creación y posicionamiento de los botones en el QGridLayout
        for row, keys in enumerate(keyBoard):
            for col, key in enumerate(keys):
                self.buttonMap[key] = QPushButton(key)
                self.buttonMap[key].setFixedSize(BUTTON_SIZE, BUTTON_SIZE)
                buttonsLayout.addWidget(self.buttonMap[key], row, col)
                
        # Añade el layout de los botones al layout general
        self.generalLayout.addLayout(buttonsLayout)

    def setDisplayText(self, text):
        """Establece el texto en la pantalla."""
        self.display.setText(text)
        self.display.setFocus()
        
    def displayText(self):
        """Obtiene el texto actual de la pantalla."""
        return self.display.text()

    def clearDisplay(self):
        """Limpia el texto de la pantalla."""
        self.setDisplayText("")


# --- EL CONTROLADOR (Manejo de Eventos) ---

class PyCalc:
    """Clase controladora de PyCalc."""
    def __init__(self, model, view):
        self._evaluate = model
        self._view = view
        self._connectSignalsAndSlots()

    def _calculateResult(self):
        """Evalúa la expresión actual y muestra el resultado."""
        result = self._evaluate(expression=self._view.displayText())
        self._view.setDisplayText(result)

    def _buildExpression(self, subExpression):
        """Construye la expresión matemática en la pantalla."""
        # Limpia la pantalla si muestra un mensaje de error
        if self._view.displayText() == ERROR_MSG:
            self._view.clearDisplay()
        
        expression = self._view.displayText() + subExpression
        self._view.setDisplayText(expression)

    def _connectSignalsAndSlots(self):
        """Conecta las señales de los botones con sus slots (métodos)."""
        for keySymbol, button in self._view.buttonMap.items():
            if keySymbol not in {"=", "C"}:
                # Conecta números y operadores a _buildExpression
                button.clicked.connect(
                    partial(self._buildExpression, keySymbol)
                )
        
        # Conecta el botón "=" y la tecla Enter para calcular el resultado
        self._view.buttonMap["="].clicked.connect(self._calculateResult)
        self._view.display.returnPressed.connect(self._calculateResult)
        
        # Conecta el botón "C" (Clear)
        self._view.buttonMap["C"].clicked.connect(self._view.clearDisplay)


# --- FUNCIÓN PRINCIPAL DE EJECUCIÓN ---

def main():
    """Función principal para ejecutar la aplicación."""
    pycalc = QApplication(sys.argv)
    
    # Crea instancias de la Vista (View)
    view = PyCalcWindow()
    view.show()
    
    # Define el Modelo (Model) y crea el Controlador (Controller)
    model = evaluateExpression
    PyCalc(model=model, view=view)
    
    # Inicia el bucle de eventos de la aplicación
    sys.exit(pycalc.exec())

if __name__ == "__main__":
    main()