from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout
from PyQt6.QtCore import Qt

from .camera_widget import CameraWidget
from .directory_choice_widget import DirectoryChoiceWidget
from .aspect_widget import AspectWidget
from .range_picker_widget import RangePickerWidget
from .status_widget import StatusWidget
from .shoot_widget import ShootWidget
from .log_widget import LogWidget

class MainWidget(QWidget):
    def __init__(self, model):
        self.model = model
        super().__init__()
        self.initialize_UI()
    
    def initialize_UI(self):
        self.directory_choice_widget = DirectoryChoiceWidget()
        self.directory_choice_widget.setContentsMargins(0,0,0,0)
        
        self.aspect_widget = AspectWidget()
        self.aspect_widget.setContentsMargins(0,0,0,0)
        
        self.camera_widget = CameraWidget()
        self.camera_widget.setContentsMargins(0,0,0,0)
        self.camera_widget.setFixedSize(640,480)
        
        self.status_widget = StatusWidget()
        
        self.range_picker_widget = RangePickerWidget()
        self.range_picker_widget.setContentsMargins(0,0,0,0)
        
        self.shoot_widget = ShootWidget()
        
        self.control_layout = QVBoxLayout()
        self.control_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter|Qt.AlignmentFlag.AlignLeft)
        self.control_layout.addWidget(self.status_widget)
        self.control_layout.addWidget(self.range_picker_widget)
        self.control_layout.addWidget(self.shoot_widget)
        
        self.log_widget = LogWidget()
        
        self.content_layout = QHBoxLayout()
        self.content_layout.addWidget(self.camera_widget)
        self.content_layout.addLayout(self.control_layout)
        
        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(self.directory_choice_widget)
        self.main_layout.addWidget(self.aspect_widget)
        self.main_layout.addLayout(self.content_layout)
        self.main_layout.addWidget(self.log_widget)
        
        self.setLayout(self.main_layout)