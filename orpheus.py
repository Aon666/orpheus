import sys
from qtpy.QtWidgets import QApplication, QMainWindow, QAbstractItemView
from pathlib import Path
from classes.mainwindow import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.setWindowTitle("Orpheus' Basket")
    window.show()
    sys.exit(app.exec())