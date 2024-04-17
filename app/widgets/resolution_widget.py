from PyQt6.QtWidgets import QWidget, QComboBox, QHBoxLayout, QLabel, QMessageBox
from PyQt6.QtCore import Qt, pyqtSignal

class ResolutionWidget(QWidget):
    
    # シグナル定義
    submitted = pyqtSignal(int)
    
    def __init__(self) -> None:
        super().__init__()
        self.initialize_UI()
    
    def initialize_UI(self) -> None:
        label = QLabel('解像度')
        
        self.resolution_combo_box = QComboBox()
        self.resolution_combo_box.addItem('320x240')
        self.resolution_combo_box.addItem('640x480')
        self.resolution_combo_box.addItem('640x360')
        self.resolution_combo_box.addItem('1280x720')
        self.resolution_combo_box.setCurrentIndex(1)
        self.resolution_combo_box.currentIndexChanged.connect(self.on_resolution_changed)
        self.submitted.emit(self.resolution_combo_box.currentIndex())
        
        self.resolution_combo_box.setDisabled(True)
        
        layout = QHBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(label)
        layout.addWidget(self.resolution_combo_box)
        self.setLayout(layout)
    
    def on_resolution_changed(self,index:int) -> None:
        self.submitted.emit(index)
        
    def on_error(self, message:str) -> None:
        QMessageBox.critical(None,"Error",message)