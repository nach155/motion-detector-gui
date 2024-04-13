from PyQt6.QtCore import QObject, pyqtSignal
import os

class RecorderModel(QObject):
    # エラーシグナル
    ## 保存先エラー
    dir_choise_error = pyqtSignal(str)
    ## 画面サイズエラー
    camera_size_error = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.directory_path = None
        self.camera_size = (640,480)
        
    ## 保存先を設定
    def set_save_directory_path(self, directory_path:str) -> None:
        if os.path.isdir(directory_path):
            self.directory_path = directory_path
        elif directory_path == "":
            self.dir_choise_error.emit("保存先を入力してください")
        else:
            self.dir_choise_error.emit("保存先を入力してください")
            
    ## カメラサイズを設定
    def set_camera_size(self, index:int) -> None:
        if index == 0:
            self.camera_size = (320,240)
        elif index == 1:
            self.camera_size = (640,480)
        elif index == 2:
            self.camera_size = (1080,720)
        else:
            self.camera_size_error.emit("値が不正です")