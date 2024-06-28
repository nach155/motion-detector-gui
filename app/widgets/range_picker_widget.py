from PyQt6.QtWidgets import QWidget, QGridLayout, QLabel, QVBoxLayout, QSpinBox, QPushButton, QHBoxLayout
from PyQt6.QtCore import Qt, pyqtSignal

class RangePickerWidget(QWidget):
    
    set_range_submitted = pyqtSignal(tuple)
    # reset_range_submitted = pyqtSignal(tuple)
    
    def __init__(self)->None:
        super().__init__()
        self.initialize_UI()
        
    def initialize_UI(self)->None:
        self.range_label = QLabel("範囲指定")
        self.range_top_left_label = QLabel("左上(x:y)")
        self.range_top_left_x = QSpinBox()
        self.range_top_left_y = QSpinBox()
        
        self.range_bottom_right_label = QLabel("右下(x:y)")
        self.range_bottom_right_x = QSpinBox()
        self.range_bottom_right_y = QSpinBox()
        
        self.range_top_left_x.setRange(0,640)
        self.range_top_left_y.setRange(0,480)
        self.range_bottom_right_x.setRange(0,640)
        self.range_bottom_right_y.setRange(0,480)
        
        self.range_bottom_right_x.setValue(640)
        self.range_bottom_right_y.setValue(480)
        
        self.range_picker_layout = QGridLayout()
        self.range_picker_layout.addWidget(self.range_top_left_label,0,0)
        self.range_picker_layout.addWidget(self.range_top_left_x,0,1)
        self.range_picker_layout.addWidget(self.range_top_left_y,0,2)
        self.range_picker_layout.addWidget(self.range_bottom_right_label,1,0)
        self.range_picker_layout.addWidget(self.range_bottom_right_x,1,1)
        self.range_picker_layout.addWidget(self.range_bottom_right_y,1,2)

        self.range_set_button = QPushButton("範囲設定",clicked=self.set_range)
        self.range_reset_button = QPushButton("範囲リセット", clicked=self.reset_range)
        
        self.button_layout = QHBoxLayout()
        self.button_layout.addWidget(self.range_set_button)
        self.button_layout.addWidget(self.range_reset_button)
                
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.range_label)
        self.layout.addLayout(self.range_picker_layout)
        self.layout.addLayout(self.button_layout)

        self.layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        self.setLayout(self.layout)
        
    def set_range(self) -> None:
        self.set_range_submitted.emit(
            ((self.range_top_left_x.value(),self.range_top_left_y.value()),
             (self.range_bottom_right_x.value(), self.range_bottom_right_y.value())))
        
    def reset_range(self) -> None:
        self.range_top_left_x.setValue(0)
        self.range_top_left_y.setValue(0)
        self.range_bottom_right_x.setValue(640)
        self.range_bottom_right_y.setValue(480)
        self.set_range_submitted.emit(((0,0),(640,480)))
        # self.reset_range_submitted.emit(((0,0),(640,480)))
    
    def set_dragend_range(self,range) -> None:
        self.range_top_left_x.setValue(range[0][0])
        self.range_top_left_y.setValue(range[0][1])
        self.range_bottom_right_x.setValue(range[1][0])
        self.range_bottom_right_y.setValue(range[1][1])