from PyQt6.QtWidgets import QWidget, QLabel
from PyQt6.QtCore import pyqtSignal, QThread, pyqtSlot
from PyQt6.QtGui import QCloseEvent, QImage, QMouseEvent, QPixmap, QPainter, QPen, QColor
import cv2

class CameraWidget(QWidget):
    def __init__(self, width:int|None=None, height:int|None=None, scale:float|None=None) -> None:
        super().__init__()
        if width is None or height is None:
            pass
        self.initialize_UI(width,height)
        
        # カメラのスレッド
        self.video_thread:VideoThread = VideoThread(width,height,scale)
        self.video_thread.change_pixmap_signal.connect(self.update_image)
        
        self.mouse_press_position = (0,0)
        self.mouse_release_position = (0,0)
        
        # self.video_thread.start()
        
    def initialize_UI(self,width:int, height:int) -> None:
        self.img_label = QLabel(self)
        self.img_label.setContentsMargins(0,0,0,0)
        self.img_label.setFixedSize(width,height)
        
    def closeEvent(self, event: QCloseEvent | None) -> None:
        self.video_thread.terminate()
        event.accept()
        
    def mousePressEvent(self, event: QMouseEvent | None) -> None:
        self.mouse_press_position = (int(event.position().x()),int(event.position().y()))
        print(self.mouse_press_position)
        return super().mousePressEvent(event)
    
    def mouseReleaseEvent(self, event: QMouseEvent | None) -> None:
        self.mouse_release_position = (int(event.position().x()),int(event.position().y()))
        print(self.mouse_release_position)        
        return super().mouseReleaseEvent(event)
    
    def _drawRectAngle(self):
        canvas = self.img_label.pixmap()
        pen = QPen()
        pen.setWidth(3)
        pen.setColor(QColor('#FF0000'))
        painter = QPainter(canvas)
        painter.setPen(pen)
        painter.drawRect(self.mouse_press_position[0],self.mouse_press_position[1], (self.mouse_release_position[0] - self.mouse_press_position[0]),(self.mouse_release_position[1] - self.mouse_press_position[1]))
        painter.end()
        self.img_label.setPixmap(canvas)
    
    @pyqtSlot(QImage)
    def update_image(self, image):
        self.img_label.setPixmap(QPixmap.fromImage(image))
        self._drawRectAngle()
        
    def on_camera_size_changed(self, size:tuple):
        # カメラを停止
        self.video_thread.stop()
        # カメラを再定義
        self.video_thread:VideoThread = VideoThread(size[0],size[1],size[2])
        self.video_thread.change_pixmap_signal.connect(self.update_image)
        self.video_thread.start()
        
        # 画面サイズを変更
        self.img_label.resize(int(size[0]*size[2]),int(size[1]*size[2]))
    
    def start_camera(self) -> None:
        print("start camera")
        self.video_thread.start()
    
    def stop_camera(self) -> None:
        print("stop camera")
        self.video_thread.stop()
        
class VideoThread(QThread):

    change_pixmap_signal = pyqtSignal(QImage)
    playing = True

    def __init__(self, width:int, height:int, scale:float) -> None:
        super().__init__()
        self.width = width
        self.height = height
        self.scale = scale
        self.cap = None
        
    def run(self) -> None:
        self.playing = True
        if self.cap is None:
            self.cap = cv2.VideoCapture(0)
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH,self.width)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT,self.height)
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
                break
        self.cap.release()
        print("camera released.")
        self.cap = None
        
    def stop(self) -> None:
        self.playing = False
        self.quit()