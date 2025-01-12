from PySide6.QtWidgets import QWidget, QLineEdit, QHBoxLayout, QPushButton, QFileDialog, QMessageBox
from PySide6.QtCore import Signal
import os

class DirectoryChoiceWidget(QWidget):

    # シグナル定義
    submitted = Signal(str)
    
    def __init__(self) -> None:
        super().__init__()
        self.initialize_UI()
        
    def initialize_UI(self):
        self.dir_name_widget = QLineEdit(f'{os.getcwd()}')
        self.dir_name_widget.setReadOnly(True)
        self.dir_name_widget.setFixedWidth(200)
        self.dir_name_button = QPushButton('保存先',clicked=self.choose_directory)
        
        self.layout = QHBoxLayout()
        self.layout.addWidget(self.dir_name_widget)
        self.layout.addWidget(self.dir_name_button)
        
        self.setLayout(self.layout)
    
    def choose_directory(self) -> None:
        directory_path = QFileDialog.getExistingDirectory(self,'open',"./")
        self.dir_name_widget.setText(directory_path)
        # モデルに送信
        self.submitted.emit(directory_path)
    
    def on_error(self,message:str) -> None:
        QMessageBox.critical(None,"Error",message)
        self.dir_name_widget.clear()