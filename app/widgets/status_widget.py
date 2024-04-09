from PyQt6.QtWidgets import QWidget, QLabel, QComboBox, QHBoxLayout

class StatusWidget(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.initialize_UI()
    
    def initialize_UI(self) -> None:
        self.status_label = QLabel("ステータス")
        self.status_combo_box = QComboBox()
        self.status_combo_box.addItem("設定中")
        self.status_combo_box.addItem("検知中")
        self.status_combo_box.setDisabled(True)
        self.layout = QHBoxLayout()
        self.layout.addWidget(self.status_label)
        self.layout.addWidget(self.status_combo_box)
        
        self.setLayout(self.layout)
        