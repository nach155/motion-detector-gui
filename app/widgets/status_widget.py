from PyQt6.QtWidgets import QWidget, QLabel, QLineEdit, QHBoxLayout, QSizePolicy
from PyQt6.QtCore import Qt

class StatusWidget(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.initialize_UI()
    
    def initialize_UI(self) -> None:
        status_label = QLabel("ステータス")
        status_label.setSizePolicy(QSizePolicy.Policy.Fixed,QSizePolicy.Policy.Fixed)
        
        self.status_text = QLineEdit("設定中")
        self.status_text.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.status_text.setSizePolicy(QSizePolicy.Policy.Fixed,QSizePolicy.Policy.Fixed)
        self.status_text.setReadOnly(True)
        
        layout = QHBoxLayout()
        layout.addWidget(status_label)
        layout.addWidget(self.status_text)
        layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        
        self.setLayout(layout)
        