from PyQt6.QtWidgets import QWidget, QGridLayout, QLabel, QVBoxLayout, QSpinBox, QPushButton, QHBoxLayout
from PyQt6.QtCore import Qt

class RangePickerWidget(QWidget):
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
        
        self.range_picker_layout = QGridLayout()
        self.range_picker_layout.addWidget(self.range_top_left_label,0,0)
        self.range_picker_layout.addWidget(self.range_top_left_x,0,1)
        self.range_picker_layout.addWidget(self.range_top_left_y,0,2)
        self.range_picker_layout.addWidget(self.range_bottom_right_label,1,0)
        self.range_picker_layout.addWidget(self.range_bottom_right_x,1,1)
        self.range_picker_layout.addWidget(self.range_bottom_right_y,1,2)

        self.range_set_button = QPushButton("範囲設定")
        self.range_reset_button = QPushButton("範囲リセット")
        
        self.button_layout = QHBoxLayout()
        self.button_layout.addWidget(self.range_set_button)
        self.button_layout.addWidget(self.range_reset_button)
                
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.range_label)
        self.layout.addLayout(self.range_picker_layout)
        self.layout.addLayout(self.button_layout)

        self.layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        self.setLayout(self.layout)
        
        