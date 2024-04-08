from PyQt6.QtWidgets import QWidget, QLineEdit, QHBoxLayout, QPushButton, QFileDialog

class DirectoryChoiceWidget(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.initialize_UI()
        
    def initialize_UI(self):
        self.dir_name_widget = QLineEdit('')
        self.dir_name_widget.setReadOnly(True)
        self.dir_name_button = QPushButton('choose directory',clicked=self.choose_directory)
        
        self.layout = QHBoxLayout()
        self.layout.addWidget(self.dir_name_widget)
        self.layout.addWidget(self.dir_name_button)
        
        self.setLayout(self.layout)
    
    def choose_directory(self) -> None:
        directory_path = QFileDialog.getExistingDirectory(self,'open',"./")
        if directory_path == '':
            return
        self.directory_path = directory_path
        self.dir_name_widget.setText(self.directory_path)