from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QHBoxLayout

class ShootWidget(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.initialize_UII()
    
    def initialize_UII(self) -> None:
        
        self.camera_start_button = QPushButton("カメラ起動")
        self.camera_stop_button = QPushButton("カメラ停止")
        camera_layout = QHBoxLayout()
        camera_layout.addWidget(self.camera_start_button)
        camera_layout.addWidget(self.camera_stop_button)
        
        self.shoot_start_button = QPushButton("検知開始")
        self.shoot_stop_button = QPushButton("検知終了")
        
        shoot_layout = QHBoxLayout()
        shoot_layout.addWidget(self.shoot_start_button)
        shoot_layout.addWidget(self.shoot_stop_button)
        
        self.layout = QVBoxLayout()
        self.layout.addLayout(camera_layout)
        self.layout.addLayout(shoot_layout)
        
        self.setLayout(self.layout)