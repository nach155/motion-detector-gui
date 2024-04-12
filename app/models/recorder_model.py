from PyQt6.QtCore import QObject, pyqtSignal
import os

class RecorderModel(QObject):
    # エラーシグナル
    dir_choise_error = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.directory_path = None
        self.camera_size = (640,480)
        
    def set_save_directory_path(self, directory_path:str) -> None:
        if os.path.isdir(directory_path):
            self.directory_path = directory_path
        elif directory_path == "":
            self.dir_choise_error.emit("保存先を入力してください")
        else:
            self.dir_choise_error.emit("保存先を入力してください")