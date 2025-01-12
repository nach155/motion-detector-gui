from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QHBoxLayout

class ShootWidget(QWidget):
    
    camera_start_submitted = Signal()
    camera_stop_submitted = Signal()
    detect_start_submitted = Signal()
    detect_stop_submitted = Signal()
    
    def __init__(self) -> None:
        super().__init__()
        self.initialize_UII()
    
    def initialize_UII(self) -> None:
        
        self.camera_start_button = QPushButton("カメラ起動",clicked=self.on_camera_start_clicked)
        self.camera_stop_button = QPushButton("カメラ停止",clicked=self.on_camera_stop_clicked)
        camera_layout = QHBoxLayout()
        camera_layout.addWidget(self.camera_start_button)
        camera_layout.addWidget(self.camera_stop_button)
        
        self.shoot_start_button = QPushButton("検知開始",clicked=self.on_detect_start_clicked)
        self.shoot_stop_button = QPushButton("検知終了",clicked=self.on_detect_stop_clicked)
        
        shoot_layout = QHBoxLayout()
        shoot_layout.addWidget(self.shoot_start_button)
        shoot_layout.addWidget(self.shoot_stop_button)
        
        self.layout = QVBoxLayout()
        self.layout.addLayout(camera_layout)
        self.layout.addLayout(shoot_layout)
        
        self.setLayout(self.layout)
        
    def on_camera_start_clicked(self) -> None:
        self.camera_start_submitted.emit()
        
    def on_camera_stop_clicked(self) -> None:
        self.camera_stop_submitted.emit()
        
    def on_detect_start_clicked(self)->None:
        self.detect_start_submitted.emit()
        
    def on_detect_stop_clicked(self)->None:
        self.detect_stop_submitted.emit()