from PyQt6.QtWidgets import QApplication
import sys

from app.main_window import MainWindow

def main():
    app = QApplication(sys.argv)
    mv = MainWindow()
    mv.show()
    app.exec()

#################################################
if __name__ == '__main__':
    main()