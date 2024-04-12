from PyQt6.QtWidgets import QWidget, QComboBox, QHBoxLayout, QLabel
from PyQt6.QtCore import Qt

class AspectWidget(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.initialize_UI()
    
    def initialize_UI(self) -> None:
        label = QLabel('縦横比')
        label.setContentsMargins(0,0,0,0)
        
        self.aspect_combo_box = QComboBox()
        self.aspect_combo_box.addItem('画面比率')
        self.aspect_combo_box.addItem('1:1')
        self.aspect_combo_box.addItem('自由比率')
        
        layout = QHBoxLayout()
        
        layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(label)
        layout.addWidget(self.aspect_combo_box)
        self.setLayout(layout)