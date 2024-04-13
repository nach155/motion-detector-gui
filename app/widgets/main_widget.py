from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout
from PyQt6.QtCore import Qt

from .camera_widget import CameraWidget
from .directory_choice_widget import DirectoryChoiceWidget
from .resolution_widget import ResolutionWidget
from .range_picker_widget import RangePickerWidget
from .status_widget import StatusWidget
from .shoot_widget import ShootWidget
from .log_widget import LogWidget
from ..models.recorder_model import RecorderModel

class MainWidget(QWidget):
    def __init__(self, model: RecorderModel) -> None:
        self.model = model
        super().__init__()
        self.initialize_UI()
        self.initialize_signal_slot()
    
    def initialize_UI(self) -> None:
        self.directory_choice_widget = DirectoryChoiceWidget()
        self.directory_choice_widget.setContentsMargins(0,0,0,0)
        
        self.resolution_widget = ResolutionWidget()
        self.resolution_widget.setContentsMargins(0,0,0,0)
        
        self.camera_widget = CameraWidget(self.model.camera_size[0],self.model.camera_size[1])
        self.camera_widget.setContentsMargins(0,0,0,0)
        self.camera_widget.setFixedSize(self.model.camera_size[0],self.model.camera_size[1])
        
        self.status_widget = StatusWidget()
        
        self.range_picker_widget = RangePickerWidget()
        self.range_picker_widget.setContentsMargins(0,0,0,0)
        
        self.shoot_widget = ShootWidget()
        
        control_layout = QVBoxLayout()
        control_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter|Qt.AlignmentFlag.AlignLeft)
        control_layout.addWidget(self.status_widget)
        control_layout.addWidget(self.range_picker_widget)
        control_layout.addWidget(self.shoot_widget)
        
        self.log_widget = LogWidget()
        
        content_layout = QHBoxLayout()
        content_layout.addWidget(self.camera_widget)
        content_layout.addLayout(control_layout)
        
        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(self.directory_choice_widget)
        self.main_layout.addWidget(self.resolution_widget)
        self.main_layout.addLayout(content_layout)
        self.main_layout.addWidget(self.log_widget)
        
        self.setLayout(self.main_layout)
        
    def initialize_signal_slot(self) -> None:
        # 保存先のディレクトリを指定する
        self.directory_choice_widget.submitted.connect(self.model.set_save_directory_path)
        self.model.dir_choise_error.connect(self.directory_choice_widget.on_error)
        
        # 