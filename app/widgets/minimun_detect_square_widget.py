from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QSpinBox
from PySide6.QtCore import Signal

class MinimumDetectSquareWidget(QWidget):
    
    set_square_submitted = Signal(int)

    def __init__(self, label_text="最小検出サイズ", min_value=1, max_value=100, default_value=30, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout(self)
        self.label = QLabel(label_text)
        self.spin_box = QSpinBox()
        self.spin_box.setRange(min_value, max_value)
        self.spin_box.setValue(default_value)
        self.spin_box.valueChanged.connect(self.changeEvent)
        layout.addWidget(self.label)
        layout.addWidget(self.spin_box)
        self.setLayout(layout)

    def value(self):
        return self.spin_box.value()

    def set_value(self, value):
        self.spin_box.setValue(value)
    
    def changeEvent(self, value):
        self.set_square_submitted.emit(value)