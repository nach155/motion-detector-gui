from PyQt6.QtCore import QObject, pyqtSignal


class RecorderModel(QObject):
    # エラーシグナル
    error = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.file_path = None
        self.camera_size = None