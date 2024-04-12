from PyQt6.QtWidgets import QWidget, QLabel, QLineEdit, QHBoxLayout
from PyQt6.QtCore import Qt

class StatusWidget(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.initialize_UI()
    
    def initialize_UI(self) -> None:
        self.status_label = QLabel("ステータス")
        self.status_text = QLineEdit("設定中")
        self.status_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_text.setReadOnly(True)
        self.layout = QHBoxLayout()
        self.layout.addWidget(self.status_label)
        self.layout.addWidget(self.status_text)
        
        self.setLayout(self.layout)
        