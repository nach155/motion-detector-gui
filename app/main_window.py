from PyQt6.QtWidgets import QMainWindow

from .models.recorder_model import RecorderModel
from .widgets.main_widget import MainWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Movement Recorder")
        self.model = RecorderModel()
        self.view = MainWidget(self.model)
        self.setCentralWidget(self.view)