from PyQt6.QtWidgets import QWidget, QLabel
from PyQt6.QtCore import pyqtSignal, QThread, pyqtSlot
from PyQt6.QtGui import QCloseEvent, QImage, QMouseEvent, QPixmap
import cv2

class CameraWidget(QWidget):
    def __init__(self, width:int|None=None, height:int|None=None, scale:float|None=None) -> None:
        super().__init__()
        if width is None or height is None:
            pass
        self.initialize_UI(width,height)
        self.thread:VideoThread = VideoThread(width,height,scale)
        self.thread.change_pixmap_signal.connect(self.update_image)
        self.thread.start()
        
    def initialize_UI(self,width:int, height:int) -> None:
        self.img_label = QLabel(self)
        self.img_label.setContentsMargins(0,0,0,0)
        self.img_label.setFixedSize(width,height)
        
        
    def closeEvent(self, event: QCloseEvent | None) -> None:
        self.thread.terminate()
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
    
    def on_camera_size_changed(self, size:tuple):
        # カメラを停止
        self.thread.stop()
        # カメラを再定義
        self.thread:VideoThread = VideoThread(size[0],size[1],size[2])
        self.thread.change_pixmap_signal.connect(self.update_image)
        self.thread.start()
        
        # 画面サイズを変更
        self.img_label.resize(int(size[0]*size[2]),int(size[1]*size[2]))
        
class VideoThread(QThread):

    change_pixmap_signal = pyqtSignal(QImage)
    playing = True

    def __init__(self, width:int, height:int, scale:float) -> None:
        super().__init__()
        # self.width = width
        # self.height = height
        self.scale = scale
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH,width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT,height)
        
    def run(self) -> None:
        while self.playing:
            ret, frame = self.cap.read()
            if ret:
                if self.scale < 1:
                    frame = cv2.resize(frame,None,fx=self.scale,fy=self.scale)
                h, w, ch = frame.shape
                bytesPerLine = frame.strides[0]
                image = QImage(frame.data, w, h, bytesPerLine, QImage.Format.Format_BGR888)
                self.change_pixmap_signal.emit(image)
            else:
                raise
        self.cap.release()

    def stop(self) -> None:
        self.playing = False
        self.terminate()