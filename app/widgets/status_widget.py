from PyQt6.QtWidgets import QWidget, QLabel, QLineEdit, QHBoxLayout
from PyQt6.QtCore import Qt

class StatusWidget(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.initialize_UI()
    
    def initialize_UI(self) -> None:
        status_label = QLabel("ステータス")
        status_label.setFixedWidth(60)
        status_label.setContentsMargins(0,0,0,0)
        
        self.status_text = QLineEdit("設定中")
        self.status_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_text.setReadOnly(True)
        self.status_text.setFixedWidth(100)
        
        layout = QHBoxLayout()
        layout.addWidget(status_label)
        layout.addWidget(self.status_text)
        layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        
        self.setLayout(layout)
        