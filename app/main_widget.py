from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout
from PySide6.QtCore import Qt

from .widgets.camera_widget import CameraWidget
from .widgets.directory_choice_widget import DirectoryChoiceWidget
from .widgets.resolution_widget import ResolutionWidget
from .widgets.range_picker_widget import RangePickerWidget
from .widgets.status_widget import StatusWidget
from .widgets.shoot_widget import ShootWidget
from .widgets.log_widget import LogWidget
from .models.recorder_model import RecorderModel

class MainWidget(QWidget):
    def __init__(self, model: RecorderModel) -> None:
        self.model = model
        super().__init__()
        self.initialize_UI()
        self.initialize_signal_slot()
    
    def initialize_UI(self) -> None:
        self.directory_choice_widget = DirectoryChoiceWidget()
        
        self.resolution_widget = ResolutionWidget()
        
        self.status_widget = StatusWidget()
        
        self.range_picker_widget = RangePickerWidget()
        
        self.shoot_widget = ShootWidget()
        
        self.log_widget = LogWidget()
        
        control_layout = QVBoxLayout()
        control_layout.addWidget(self.directory_choice_widget)
        control_layout.addWidget(self.resolution_widget)
        control_layout.addWidget(self.status_widget)
        control_layout.addWidget(self.range_picker_widget)
        control_layout.addWidget(self.shoot_widget)
        control_layout.addWidget(self.log_widget)
        
        self.camera_widget = CameraWidget(self.model.camera_size[0],self.model.camera_size[1],self.model.camera_size[2])
        self.camera_widget.setContentsMargins(0,0,0,0)
        self.camera_widget.setFixedSize(self.model.camera_size[0]*self.model.camera_size[2],self.model.camera_size[1]*self.model.camera_size[2])

        self.main_layout = QHBoxLayout()
        self.main_layout.addWidget(self.camera_widget)
        self.main_layout.addLayout(control_layout)

        self.setLayout(self.main_layout)
        
    def initialize_signal_slot(self) -> None:
        # 保存先のディレクトリを指定する
        self.directory_choice_widget.submitted.connect(self.model.set_save_directory_path)
        self.model.dir_choise_notifier.connect(self.camera_widget.set_save_dir)
        self.model.dir_choise_error.connect(self.directory_choice_widget.on_error)
        
        # カメラの解像度を切り替える
        self.resolution_widget.submitted.connect(self.model.set_camera_size)
        # self.model.camera_size_notifier.connect(self.camera_widget.on_camera_size_changed)
        # self.model.camera_size_notifier.connect(self.set_camera_widget_size)
        
        # カメラスタートを押す
        self.shoot_widget.camera_start_submitted.connect(self.model.set_camera_start)
        self.model.camera_start_notifier.connect(self.camera_widget.start_camera)
        
        # カメラストップ押す
        self.shoot_widget.camera_stop_submitted.connect(self.model.set_camera_stop)
        self.model.camera_stop_notifier.connect(self.camera_widget.stop_camera)
        
        # 範囲設定を押す or 範囲選択リセットを押す
        self.range_picker_widget.set_range_submitted.connect(self.model.set_detect_range)
        self.model.detect_range_notifier.connect(self.camera_widget.set_detect_range)
        
        # ドラッグ&ドロップで範囲指定
        self.camera_widget.dragend_submitted.connect(self.model.set_dragend_range)
        self.model.dragend_notifier.connect(self.range_picker_widget.set_dragend_range)
        
        # 検知開始押す
        self.shoot_widget.detect_start_submitted.connect(self.model.set_detect_start)
        self.model.detect_start_notifier.connect(self.camera_widget.start_detect)
        self.model.detect_start_notifier.connect(self.status_widget.set_detect_start_status)

        # 検知終了押す
        self.shoot_widget.detect_stop_submitted.connect(self.model.set_detect_stop)
        self.model.detect_stop_notifier.connect(self.camera_widget.stop_detect)
        self.model.detect_stop_notifier.connect(self.status_widget.set_detect_stop_status)
        
        # ログ関連
        self.camera_widget.log_submitted.connect(self.model.append_log)
        self.model.log_append_notifier.connect(self.log_widget.append_log)
        
    # def set_camera_widget_size(self,size:tuple):
    #     self.camera_widget.resize(int(size[0]*size[2]),int(size[1]*size[2]))
    #     print(self.camera_widget.size())
    