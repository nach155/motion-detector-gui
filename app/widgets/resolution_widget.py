from PyQt6.QtWidgets import QWidget, QComboBox, QHBoxLayout, QLabel
from PyQt6.QtCore import Qt

class ResolutionWidget(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.initialize_UI()
    
    def initialize_UI(self) -> None:
        label = QLabel('解像度')
        label.setContentsMargins(0,0,0,0)
        
        self.aspect_combo_box = QComboBox()
        self.aspect_combo_box.addItem('320x240')
        self.aspect_combo_box.addItem('640x480')
        self.aspect_combo_box.addItem('1080x720')
        self.aspect_combo_box.setCurrentIndex(1)
        
        layout = QHBoxLayout()
        
        layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(label)
        layout.addWidget(self.aspect_combo_box)
        self.setLayout(layout)