from PyQt6.QtWidgets import QWidget, QVBoxLayout

from .camera_widget import CameraWidget
from .directory_choice_widget import DirectoryChoiceWidget

class MainWidget(QWidget):
    def __init__(self, model):
        self.model = model
        super().__init__()
        self.initialize_UI()
    
    def initialize_UI(self):
        self.directory_choice_widget = DirectoryChoiceWidget()
        self.directory_choice_widget.setContentsMargins(0,0,0,0)
        
        self.camera_widget = CameraWidget()
        self.camera_widget.setContentsMargins(0,0,0,0)
        self.camera_widget.setFixedSize(640,480)
        
        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(self.directory_choice_widget)
        self.main_layout.addWidget(self.camera_widget)
        
        self.setLayout(self.main_layout)