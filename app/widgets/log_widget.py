from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QTextEdit, QVBoxLayout

class LogWidget(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.initialize_UI()
        
    def initialize_UI(self) -> None:
        self.log_textarea = QTextEdit()
        self.layout:QVBoxLayout = QVBoxLayout()
        self.layout.addWidget(self.log_textarea)
        
        self.setLayout(self.layout)
        
    def append_log(self, log:str) -> None:
        self.log_textarea.append(log)