from PyQt6.QtWidgets import QWidget, QLabel
from PyQt6.QtCore import pyqtSignal, QThread, pyqtSlot
from PyQt6.QtGui import QCloseEvent, QImage, QMouseEvent, QPixmap
import cv2

class CameraWidget(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.initialize_UI()
        self.thread = VideoThread()
        self.thread.change_pixmap_signal.connect(self.update_image)
        self.thread.start()
    
    def initialize_UI(self) -> None:
        self.img_label = QLabel(self)
        self.img_label.setContentsMargins(0,0,0,0)
        self.img_label.setFixedSize(640,480)
        
        
    def closeEvent(self, event: QCloseEvent | None) -> None:
        self.thread.stop()
        event.accept()
        
    def mousePressEvent(self, event: QMouseEvent | None) -> None:
        self.mouse_press_position = (int(event.position().x()),int(event.position().y()))
        return super().mousePressEvent(event)
    
    def mouseReleaseEvent(self, event: QMouseEvent | None) -> None:
        self.mouse_release_position = (int(event.position().x()),int(event.position().y()))
        return super().mouseReleaseEvent(event)
    
    @pyqtSlot(QImage)
    def update_image(self, image):
        self.img_label.setPixmap(QPixmap.fromImage(image))
        
class VideoThread(QThread):

    change_pixmap_signal = pyqtSignal(QImage)
    playing = True

    def run(self) -> None:
        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH,640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT,480)
        while self.playing:
            ret, frame = cap.read()
            if ret:
                h, w, ch = frame.shape
                bytesPerLine = frame.strides[0]
                image = QImage(frame.data, w, h, bytesPerLine, QImage.Format.Format_BGR888)
                self.change_pixmap_signal.emit(image)
        cap.release()

    def stop(self) -> None:
        self.playing = False
        self.wait()