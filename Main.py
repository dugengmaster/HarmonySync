from PyQt6.QtWidgets import QMainWindow, QApplication, QHBoxLayout, QVBoxLayout, QWidget
from Gui.ExplorerBar import ExplorerBar
from Gui.Waveform_Editor import Waveform_Editor
from Gui.MidiWriteArea import MidiWriteArea

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("HarmonySync")
        self.setMinimumSize(1355, 930)
        self.init_ui()
    
    def init_ui(self):
        self.hbox = QWidget(self)         
        self.hbox.setGeometry(0, 0, 1400, 500)
        
        self.h_layout = QHBoxLayout(self.hbox)
        explorer = ExplorerBar()
        wave_editor = Waveform_Editor()
        self.h_layout.addWidget(explorer)
        self.h_layout.addSpacing(-770)
        self.h_layout.addWidget(wave_editor)
        
        self.vbox = QWidget(self)
        self.vbox.setGeometry(0, 510, 1400, 500)

        self.v_layout = QVBoxLayout(self.vbox)
        midi_area = MidiWriteArea()
        self.v_layout.addWidget(midi_area)
        
if __name__ == "__main__":
    app = QApplication([])
    Main = MainWindow()
    Main.show()
    app.exec()