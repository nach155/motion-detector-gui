from PySide6.QtWidgets import QWidget, QLabel
from PySide6.QtCore import Signal, QThread, Slot
from PySide6.QtGui import QCloseEvent, QImage, QMouseEvent, QPixmap, QPainter, QPen, QColor
import cv2, datetime, os, time
import numpy as np
from picamera2 import Picamera2

class CameraWidget(QWidget):
    
    dragend_submitted = Signal(tuple)
    movement_submitted = Signal(bool)
    
    log_submitted = Signal(str)
    
    def __init__(self, width:int|None=None, height:int|None=None, scale:float|None=None) -> None:
        super().__init__()
        if width is None or height is None:
            pass
        self.initialize_UI(width,height)
        
        # カメラのスレッド
        self.video_thread:VideoThread = VideoThread(width,height,scale,10)
        self.video_thread.frame_signal.connect(self.update_image)
        
        self.mouse_press_position = (0,0)
        self.mouse_release_position = (640,480)
        self.detect_range = (self.mouse_press_position,self.mouse_release_position)
        
        # 録画
        self.recorder = VideoRecorder(os.getcwd(),width,height,10)
        
        # 動体検知
        self.is_detecting = False
        self.previous_frame = None
        self.start_camera()
        
    def initialize_UI(self,width:int, height:int) -> None:
        self.img_label = QLabel(self)
        self.img_label.setContentsMargins(0,0,0,0)
        self.img_label.setFixedSize(width,height)
        
        self.pen = QPen()
        self.pen.setWidth(3)
        self.pen.setColor(QColor('#FF0000'))
        
    def closeEvent(self, event: QCloseEvent | None) -> None:
        self.video_thread.terminate()
        event.accept()
        
    def mousePressEvent(self, event: QMouseEvent | None) -> None:
        self.mouse_press_position = self.mouse_release_position = (int(event.position().x()),int(event.position().y()))
        return super().mousePressEvent(event)
    
    def mouseReleaseEvent(self, event: QMouseEvent | None) -> None:
        self.mouse_release_position = (min(int(event.position().x()),640),min(int(event.position().y()),480))
        self.dragend_submitted.emit(
            (self.mouse_press_position,
             self.mouse_release_position)
        )
        self.detect_range = (
            self.mouse_press_position,
            self.mouse_release_position
        )
        self.previous_frame = None
        return super().mouseReleaseEvent(event)
    
    def mouseMoveEvent(self, event: QMouseEvent | None) -> None:
        self.mouse_release_position = (min(int(event.position().x()),640),min(int(event.position().y()),480))
        return super().mouseMoveEvent(event)
    
    def _drawRectAngle(self):
        canvas = self.img_label.pixmap()
        painter = QPainter(canvas)
        painter.setPen(self.pen)
        painter.drawRect(
            self.mouse_press_position[0],
            self.mouse_press_position[1], 
            (self.mouse_release_position[0] - self.mouse_press_position[0]),
            (self.mouse_release_position[1] - self.mouse_press_position[1])
        )
        painter.end()
        self.img_label.setPixmap(canvas)
    
    @Slot(np.ndarray)
    def update_image(self, frame:np.ndarray):
        current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cv2.putText(frame, current_time, (20,20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255,255), 1, cv2.LINE_AA)
        original_frame = np.copy(frame)        
        result_frame, movement = self.move_recognize(frame)
        if self.is_detecting:
            if movement:
                self.recorder.last_movement_time = time.time()
                if self.recorder.writer is None:
                    self.recorder.setup_recorder()
                    self.log_submitted.emit(f"録画開始 : {current_time}")
            if self.recorder.writer is not None:
                self.recorder.append_frame(original_frame)
                if self.recorder.stop_more_than_margin_time():
                    self.recorder.recorder_release()
                    self.log_submitted.emit(f"録画終了 : {current_time}")
        
        elif self.recorder.writer is not None:
                self.recorder.recorder_release()
                self.log_submitted.emit(f"録画終了 : {current_time}")
                
        self.img_label.setPixmap(QPixmap.fromImage(self.cv_to_QImage(result_frame)))
        self._drawRectAngle()
        
    def QImage_to_cv(self, qimage:QImage):
        w, h, d = qimage.size().width(), qimage.size().height(), qimage.depth()
        bytes_ = qimage.bits().asstring(w * h * d // 8)
        arr = np.frombuffer(bytes_, dtype=np.uint8).reshape((h, w, d // 8))
        return arr
    
    def cv_to_QImage(self, frame:np.ndarray):
        h, w, ch = frame.shape
        bytesPerLine = frame.strides[0]
        image = QImage(frame.data, w, h, bytesPerLine, QImage.Format.Format_RGBX8888)
        return image
        
    def on_camera_size_changed(self, size:tuple):
        # カメラを停止
        self.video_thread.stop()
        # カメラを再定義
        self.video_thread:VideoThread = VideoThread(size[0],size[1],size[2])
        self.video_thread.frame_signal.connect(self.update_image)
        self.video_thread.start()
        
        # 画面サイズを変更
        self.img_label.resize(int(size[0]*size[2]),int(size[1]*size[2]))
    
    def start_camera(self) -> None:
        print("start camera")
        self.video_thread.start()
    
    def stop_camera(self) -> None:
        print("stop camera")
        self.video_thread.stop()
    
    ## 範囲設定ボタンを押した時
    def set_detect_range(self, range:tuple) -> None:
        self.mouse_press_position = range[0]
        self.mouse_release_position = range[1]
        self.detect_range = range
        self.previous_frame = None
        
    ## 動体検知
    def move_recognize(self, frame: np.ndarray) -> tuple[np.ndarray,bool]:
        # 画像をトリミング
        trim = frame[
            self.detect_range[0][1]:self.detect_range[1][1],
            self.detect_range[0][0]:self.detect_range[1][0],
        ]
        # グレースケールに変換
        trim_gray= cv2.cvtColor(trim,cv2.COLOR_BGR2GRAY)
        movement = False
        if self.previous_frame is None:
            self.previous_frame = trim_gray.copy().astype("float")
            return frame , movement
        # 現在のフレームと移動平均との差を計算
        cv2.accumulateWeighted(trim_gray, self.previous_frame, 0.8)
        frameDelta = cv2.absdiff(trim_gray, cv2.convertScaleAbs(self.previous_frame))

        # デルタ画像を閾値処理を行う
        thresh = cv2.threshold(frameDelta, 3, 255, cv2.THRESH_BINARY)[1]
        
        #輪郭のデータを得る
        contours = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]

        # 差分があった点を画面に描く
        for target in contours:
            x, y, w, h = cv2.boundingRect(target)
            x = x + self.detect_range[0][0]
            y = y + self.detect_range[0][1]
            if w < 30 or h < 30: continue # 小さな変更点は無視
            if not movement:
                movement = not movement
                # break
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0,255,0), 2)
        # 認識範囲を表示
        # cv2.rectangle(frame,(start_x,start_y),(end_x,end_y),RECOGNIZE_RANGE_COLOR,2)
        return frame, movement
        
    ## 保存先
    def set_save_dir(self, directory_path: str) -> None:
        self.recorder.set_save_dir(directory_path)
    
    ## 検知開始
    def start_detect(self)->None:
        self.is_detecting = True
    
    ## 検知終了
    def stop_detect(self)->None:
        self.is_detecting = False
    
    
class VideoThread(QThread):

    # change_pixmap_signal = Signal(QImage)
    frame_signal = Signal(np.ndarray)
    playing = True

    def __init__(self, width:int, height:int, scale:float,fps:int) -> None:
        super().__init__()
        self.width = width
        self.height = height
        self.scale = scale
        self.fps = fps
        self.cap = None
        
    def run(self) -> None:
        self.playing = True
        if self.cap is None:
            self.cap = Picamera2()
            self.cap.configure(self.cap.create_preview_configuration(
                main={
                    # "format":'XRGB8888',
                    "size":(self.width,self.height),
                },
                controls={"FrameRate":self.fps}
            ))
            self.cap.start()
            # self.cap = cv2.VideoCapture(0)
            # self.cap.set(cv2.CAP_PROP_FRAME_WIDTH,self.width)
            # self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT,self.height)
        while self.playing:
            # ret, frame = self.cap.read()
            frame = self.cap.capture_array()
            # if ret:
            if self.scale < 1:
                frame = cv2.resize(frame,None,fx=self.scale,fy=self.scale)
            self.frame_signal.emit(frame)
                
            # else:
            #     break
        self.cap.release()
        print("camera released.")
        self.cap = None
        
    def stop(self) -> None:
        self.playing = False
        self.quit()
        
class VideoRecorder(object):
    def __init__(self,save_dir:str, width:int, height:int, fps:int)->None:
        self.save_dir = save_dir
        self.width = width
        self.height = height
        self.fps = fps
        self.margin_time = 5
        self.writer = None
        self.last_movement_time = None
        self.init_recording_time = None
        self.is_recording = False
    
    def set_save_dir(self, save_dir:str)->None:
        self.save_dir = save_dir
        
    def setup_recorder(self) -> None:
        print("recorder setup")
        self.is_recording = True
        file_name = f"{self.save_dir}/{datetime.datetime.fromtimestamp(int(time.time())).strftime('%Y-%m-%d-%H_%M_%S')}.avi"
        self.writer = cv2.VideoWriter(file_name, cv2.VideoWriter_fourcc('D', 'I', 'V', '3'), self.fps, (self.width,self.height))
        self.init_recording_time = time.time()
        
    def recorder_release(self) -> None:
        print("recorder release")
        self.is_recording = False
        self.writer.release()
        self.writer = None
    
    def append_frame(self, frame:np.ndarray) -> None:
        self.writer.write(frame)
    
    def stop_more_than_margin_time(self) -> bool:
        return (time.time() - self.last_movement_time) > self.margin_time