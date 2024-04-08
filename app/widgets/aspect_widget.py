from PyQt6.QtWidgets import QWidget, QComboBox, QHBoxLayout, QLabel, QSizePolicy, QStyle
from PyQt6.QtCore import Qt

class AspectWidget(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.initialize_UI()
    
    def initialize_UI(self) -> None:
        self.label = QLabel('縦横比')
        self.label.setContentsMargins(0,0,0,0)
        
        self.aspect_combo_box = QComboBox()
        self.aspect_combo_box.addItem('a')
        self.aspect_combo_box.addItem('b')
        self.aspect_combo_box.addItem('c')
        self.aspect_combo_box.addItem('d')
        
        layout = QHBoxLayout()
        
        layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(self.label)
        layout.addWidget(self.aspect_combo_box)
        self.setLayout(layout)