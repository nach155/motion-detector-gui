from PyQt6.QtCore import QObject, pyqtSignal
import os

class RecorderModel(QObject):
    ## 保存先エラー
    dir_choise_error = pyqtSignal(str)
    ## 保存先
    dir_choise_notifier = pyqtSignal(str)
    ## 画面サイズエラー
    camera_size_error = pyqtSignal(str)
    camera_size_notifier = pyqtSignal(tuple)
    ## カメラスタート
    camera_start_notifier = pyqtSignal()
    ## カメラストップ
    camera_stop_notifier = pyqtSignal()
    ## 検知範囲
    detect_range_notifier = pyqtSignal(tuple)
    dragend_notifier = pyqtSignal(tuple)
    
    def __init__(self):
        super().__init__()
        self.directory_path = os.getcwd()
        self.camera_size = (640,480,1)
        self.camera_start = False
        
        self.detect_range = ((0,0),(640,480))
        
    ## 保存先を設定
    def set_save_directory_path(self, directory_path:str) -> None:
        if os.path.isdir(directory_path):
            self.directory_path = directory_path
            self.dir_choise_notifier.emit(directory_path)
        elif directory_path == "":
            self.dir_choise_error.emit("保存先を入力してください")
        else:
            self.dir_choise_error.emit("保存先を入力してください")
            
    ## カメラサイズを設定
    def set_camera_size(self, index:int) -> None:

        if index == 0:
            self.camera_size = (640,480,0.5)
        elif index == 1:
            self.camera_size = (640,480,1)
        elif index == 2:
            self.camera_size = (1280,720,0.5)
        elif index == 3:
            self.camera_size = (1280,720,1)
        else:
            self.camera_size_error.emit("値が不正です")
            return
        self.camera_size_notifier.emit(self.camera_size)
        
    ## カメラスタート
    def set_camera_start(self) -> None:
        self.camera_start = True
        self.camera_start_notifier.emit()
    
    ## カメラ停止
    def set_camera_stop(self) -> None:
        self.camera_start = False
        self.camera_stop_notifier.emit()
    
    ## 検知範囲を変更
    def set_detect_range(self, range) -> None:
        self.detect_range = range
        print("set detect range")
        self.detect_range_notifier.emit(self.detect_range)

    ## 検知範囲を変更(ドラッグ&ドロップ)
    def set_dragend_range(self, range) -> None:
        self.detect_range = range
        self.dragend_notifier.emit(self.detect_range)