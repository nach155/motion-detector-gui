from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QPushButton, QVBoxLayout

class ShootWidget(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.initialize_UII()
    
    def initialize_UII(self) -> None:
        
        self.camera_start_button = QPushButton("カメラ起動")
        
        self.shoot_start_button = QPushButton("検知開始")
        self.shoot_stop_button = QPushButton("検知終了")
        
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.camera_start_button)
        self.layout.addWidget(self.shoot_start_button)
        self.layout.addWidget(self.shoot_stop_button)
        
        self.setLayout(self.layout)