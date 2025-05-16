# motion-detector-gui
動体検知録画GUI
this gui shoots a movie when its camera detect motion

## depends on
* PySide6
* opencv-python
* numpy

## How to use
カメラが動く物体を検知して自動で録画をおこないます \
検知範囲はドラッグ&ドロップもしくは入力ボックスで設定することができます \
最後に動きを検知してから5秒経過したら録画を終了してファイルに書き出します


## install
```
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```