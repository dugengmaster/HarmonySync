from PyQt6 import QtWidgets, QtMultimedia
from PyQt6.QtWidgets import QWidget, QLabel, QPushButton, QGraphicsProxyWidget
from PyQt6.QtGui import QPixmap, QIcon, QDragEnterEvent, QDropEvent, QDragLeaveEvent, QFont
from PyQt6.QtCore import pyqtSignal, QFileInfo, QUrl
import librosa
import librosa.display
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
 

class Button(QPushButton):
    actionChanged = pyqtSignal(bool)

    def __init__(self, parent=None):
        super(Button, self).__init__(parent)
        self.setIconSize(self.size())
        self.original_style = self.styleSheet()
        self.setAcceptDrops(True)
        self.action = False
        self.file_url = None
    # 拖曳進入範圍事件
    def dragEnterEvent(self, event: QDragEnterEvent):
        file_url = event.mimeData().urls()[0].toLocalFile()
        mime_data = event.mimeData()
        if mime_data.hasUrls() and len(mime_data.urls()) == 1 and file_url.lower().endswith(('.wav', '.mp3')):
            event.acceptProposedAction()
            self.setStyleSheet("""border: 2px solid #4d4d4d; 
                                  border-radius: 5px; 
                                  background-color: #77DDFF; 
                                  color: #ffffff;""")
    # 拖曳離開範圍事件
    def dragLeaveEvent(self, event: QDragLeaveEvent):
        self.setStyleSheet(self.original_style)
    # 拖曳放開事件
    def dropEvent(self, event: QDropEvent):
        self.file_url = event.mimeData().urls()[0].toLocalFile()
        mime_data = event.mimeData()
        event.acceptProposedAction()
        if mime_data.hasUrls() and len(mime_data.urls()) == 1 and self.file_url.lower().endswith(('.wav', '.mp3')):
            self.setStyleSheet(self.original_style)
            self.actionChanged.emit(True)
            

class Waveform_Editor(QWidget):
    def __init__(self, parent=None):
        super(Waveform_Editor, self).__init__(parent)
        
        self.setGeometry(0, 0, 1040, 472)
        self.icon = QPixmap("gui/icon/icon3.png")
        self.audio_path1 = None
        self.audio_path2 = None
        self.init_ui()

    def init_ui(self):
        # CD槽(上)
        self.MusicButton1 = Button(self)
        self.MusicButton1.setGeometry(12, 10, 1005, 200)
        self.MusicButton1.setIcon(QIcon(self.icon.copy(0, 128, 64, 64)))
        self.MusicButton1.actionChanged.connect(self.action_changed_1)
        # 播放器外框(上)
        self.hide_Musiclabel1 = QLabel(self)
        self.hide_Musiclabel1.hide()
        self.hide_Musiclabel1.setGeometry(12, 10, 1005, 200)
        self.hide_Musiclabel1.setStyleSheet("""
                                  border: 1px solid #737373; 
                                  background-color: #D9D9D9; 
                                  color: #ffffff;
                                  """)
        # 音樂檔檔名標籤(上)
        self.name_label1 = QLabel(self)
        self.name_label1.hide()
        self.name_label1.setGeometry(20, 167, 500, 32)
        font = QFont()
        font.setBold(True)  # 設定文字為粗體
        font.setPointSize(12)  # 設定文字大小
        self.name_label1.setFont(font)
        self.name_label1.setStyleSheet("color: blue;")
        # 音波圖(上)
        self.canvas1 = FigureCanvas(plt.Figure(figsize=(10, 2)))
        self.scene1 = QtWidgets.QGraphicsScene()
        self.scene1.setSceneRect(20, 20, 980, 120)
        self.proxy_widget1 = QGraphicsProxyWidget()
        self.proxy_widget1.setWidget(self.canvas1)
        self.scene1.addItem(self.proxy_widget1)
        self.sview1 = QtWidgets.QGraphicsView(self)
        self.sview1.setGeometry(20, 20, 990, 140)
        self.sview1.hide()
        # 清除鍵(上)
        self.clear_button1 = QPushButton(self)
        self.clear_button1.hide()
        self.clear_button1.setGeometry(976, 167, 32, 32)
        self.clear_button1.setIcon(QIcon(self.icon.copy(192, 0, 64, 64)))
        self.clear_button1.setIconSize(self.clear_button1.size())
        self.clear_button1.clicked.connect(self.clear1)
        # 播放器(上)
        self.player1 = QtMultimedia.QMediaPlayer()
        self.audio_output1 = QtMultimedia.QAudioOutput()
        self.player1.setAudioOutput(self.audio_output1)
        self.audio_output1.setVolume(50)
        # CD槽(下)
        self.MusicButton2 = Button(self)
        self.MusicButton2.setGeometry(12, 220, 1005, 200)
        self.MusicButton2.setIcon(QIcon(self.icon.copy(0, 128, 64, 64)))
        self.MusicButton2.actionChanged.connect(self.action_changed_2)
        # 播放器外框(下)
        self.hide_Musiclabel2 = QLabel(self)
        self.hide_Musiclabel2.hide()
        self.hide_Musiclabel2.setGeometry(12, 220, 1005, 200)
        self.hide_Musiclabel2.setStyleSheet("""
                                  border: 1px solid #737373; 
                                  background-color: #D9D9D9; 
                                  color: #ffffff;
                                  """)
        # 音樂檔檔名標籤(下)
        self.name_label2 = QLabel(self)
        self.name_label2.hide()
        self.name_label2.setGeometry(20, 377, 500, 32)
        font = QFont()
        font.setBold(True)  # 設定文字為粗體
        font.setPointSize(12)  # 設定文字大小
        self.name_label2.setFont(font)
        self.name_label2.setStyleSheet("color: blue;")
        # 音波圖(下)
        self.canvas2 = FigureCanvas(plt.Figure(figsize=(10, 2)))
        self.scene2 = QtWidgets.QGraphicsScene()
        self.scene2.setSceneRect(20, 230, 980, 120)
        self.proxy_widget2 = QGraphicsProxyWidget()
        self.proxy_widget2.setWidget(self.canvas2)
        self.scene2.addItem(self.proxy_widget2)
        self.sview2 = QtWidgets.QGraphicsView(self)
        self.sview2.setGeometry(20, 230, 990, 140)
        self.proxy_widget2.setPos(0,210)
        self.sview2.hide()
        # 清除鍵(下)
        self.clear_button2 = QPushButton(self)
        self.clear_button2.hide()
        self.clear_button2.setGeometry(976, 377, 32, 32)
        self.clear_button2.setIcon(QIcon(self.icon.copy(192, 0, 64, 64)))
        self.clear_button2.setIconSize(self.clear_button2.size())
        self.clear_button2.clicked.connect(self.clear2)
        # 播放器(下)
        self.player2 = QtMultimedia.QMediaPlayer()
        self.audio_output2 = QtMultimedia.QAudioOutput()
        self.player2.setAudioOutput(self.audio_output2)
        self.audio_output2.setVolume(50)

        # 播放鍵
        self.play_button = QPushButton(self)
        self.play_button.setGeometry(14, 430, 32, 32)
        self.play_button.setIcon(QIcon(self.icon.copy(0, 0, 64, 64)))
        self.play_button.setIconSize(self.play_button.size())
        self.play_button.clicked.connect(self.play_audio)
        # 暫停鍵
        self.pause_button = QPushButton(self)
        self.pause_button.setGeometry(52, 430, 32, 32)
        self.pause_button.setIcon(QIcon(self.icon.copy(64, 0, 64, 64)))
        self.pause_button.setIconSize(self.pause_button.size())
        self.pause_button.clicked.connect(self.pause_audio)
        # 停止鍵
        self.stop_button = QPushButton(self)
        self.stop_button.setGeometry(90, 430, 32, 32)
        self.stop_button.setIcon(QIcon(self.icon.copy(128, 0, 64, 64)))
        self.stop_button.setIconSize(self.stop_button.size())
        self.stop_button.clicked.connect(self.stop_audio)
        # 音量旋鈕(上)
        self.volume_dial1 = QtWidgets.QDial(self)
        self.volume_dial1.setGeometry(150, 420, 48, 48)
        self.volume_dial1.setRange(0, 100)
        self.volume_dial1.setValue(50)
        self.volume_dial1.valueChanged.connect(self.update_volume1)
        # 音量旋鈕(下)
        self.volume_dial2 = QtWidgets.QDial(self)
        self.volume_dial2.setGeometry(200, 420, 48, 48)
        self.volume_dial2.setRange(0, 100)
        self.volume_dial2.setValue(50)
        self.volume_dial2.valueChanged.connect(self.update_volume2)

    # 轉換用(上)
    def action_changed_1(self, value):
        if value == True:
            # 隱藏
            self.MusicButton1.hide()
            # 顯示
            self.hide_Musiclabel1.show()
            self.audio_path1 = self.MusicButton1.file_url
            self.audioName = QFileInfo(self.MusicButton1.file_url).fileName()
            self.name_label1.show()
            self.name_label1.setText(self.audioName)
            #self.name_label1.raise_()
            self.clear_button1.show()
            # 音樂播放器與音波圖
            self.player1.setSource(QUrl.fromLocalFile(self.audio_path1))
            print("audio_path1 "+str(self.audio_path1))
            self.sview1.show() 
            self.sinWave1(self.audio_path1)
            self.sview1.setScene(self.scene1)
            self.stop_audio()
    # 轉換用(下)
    def action_changed_2(self, value):
        if value == True:
            # 隱藏
            self.MusicButton2.hide() 
            # 顯示
            self.hide_Musiclabel2.show()
            self.audio_path2 = self.MusicButton2.file_url
            self.audioName2 = QFileInfo(self.MusicButton2.file_url).fileName()
            self.name_label2.show()
            self.name_label2.setText(self.audioName2)
            self.name_label2.raise_()            
            self.clear_button2.show()
            # 音樂播放器與音波圖
            self.player2.setSource(QUrl.fromLocalFile(self.audio_path2))
            print("audio_path2 "+str(self.audio_path2))
            self.sview2.show()
            self.sinWave2(self.audio_path2)
            self.sview2.setScene(self.scene2)
            self.stop_audio()

    # 音波圖(上)
    def sinWave1(self, file_path1):
        # 讀取音檔
        y1, sr1 = librosa.load(file_path1)
        # 繪製音波圖
        fig1, ax1 = plt.subplots(figsize=(10, 2))
        librosa.display.waveshow(y1, sr=sr1, ax=ax1, color="b")
        ax1.set_xticks([])  # 隱藏 X 軸刻度
        ax1.set_yticks([])  # 隱藏 Y 軸刻度
        ax1.axis('off')
        # 使用 subplots_adjust 來微調子圖的位置
        plt.subplots_adjust(left=-0.031, right=1.04, bottom=0.25, top=0.95)
        self.canvas1.figure = fig1
        self.canvas1.draw()
    # 音波圖(下)
    def sinWave2(self, file_path2):
        # 讀取音檔
        y2, sr2 = librosa.load(file_path2)
        # 繪製音波圖
        fig2, ax2 = plt.subplots(figsize=(10, 2))
        librosa.display.waveshow(y2, sr=sr2, ax=ax2, color="b")
        ax2.set_xticks([])  # 隱藏 X 軸刻度
        ax2.set_yticks([])  # 隱藏 Y 軸刻度
        ax2.axis('off')
        # 使用 subplots_adjust 來微調子圖的位置
        plt.subplots_adjust(left=-0.031, right=1.04, bottom=0.25, top=0.95)
        self.canvas2.figure = fig2
        self.canvas2.draw()
        
    # 播放用
    def play_audio(self):
        self.player1.play()
        self.player2.play()
    # 暫停用
    def pause_audio(self):
        self.player1.pause()
        self.player2.pause()
    # 終止用
    def stop_audio(self):
        self.player1.stop()
        self.player2.stop()
    # 音量調整(上)
    def update_volume1(self):
        volume1 = self.volume_dial1.value() / 100.0
        self.audio_output1.setVolume(volume1)
    # 音量調整(下)
    def update_volume2(self):
        volume2 = self.volume_dial2.value() / 100.0
        self.audio_output2.setVolume(volume2)
    # 清除用(上)
    def clear1(self):
        self.MusicButton1.show()
        self.name_label1.hide()
        self.sview1.hide()
        self.hide_Musiclabel1.hide()
        self.clear_button1.hide()
        self.audio_path1 = None
        self.player1.stop()
        self.canvas1.figure.clear()

    # 清除用(下)
    def clear2(self):
        self.MusicButton2.show()
        self.name_label2.hide()
        self.sview2.hide()
        self.hide_Musiclabel2.hide()
        self.clear_button2.hide()
        self.audio_path2 = None
        self.player2.stop()
        self.canvas2.figure.clear()


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = Waveform_Editor()
    window.show()
    app.exec()