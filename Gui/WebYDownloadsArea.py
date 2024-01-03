from PyQt6.QtWidgets import QWidget, QTextEdit, QApplication
from PyQt6.QtGui import QFont

class MidiWriteArea(QWidget):
    def __init__(self, parent=None):
        super(MidiWriteArea, self).__init__(parent)
        
        self.setGeometry(100, 100, 1380, 400)
        self.init_ui()
    
    def init_ui(self):
        # 創建一個文字輸入框
        text_area = QTextEdit(self)
        text_area.setGeometry(10, 10, 1315, 380)

        font = QFont()
        font.setPointSize(16)
        text_area.setFont(font)

# 範例用法
if __name__ == "__main__":
    app = QApplication([])
    midi_write_area = MidiWriteArea()
    midi_write_area.show()
    app.exec()
