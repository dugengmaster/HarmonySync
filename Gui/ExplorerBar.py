from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QWidget, QFileDialog, QTreeView, QPushButton
from PyQt6.QtGui import QFileSystemModel
from PyQt6.QtCore import QDir, Qt

class ExplorerBar(QWidget):
    def __init__(self, parent=None):
        super(ExplorerBar, self).__init__(parent)
        self.setGeometry(0, 0, 320, 475)
        self.init_ui()

    def init_ui(self):
        #設置"選擇資料夾"按鍵
        self.button = QPushButton(self)
        self.button.setGeometry(9, 433, 302, 30)
        self.button.setText("選擇資料夾")
        self.button.clicked.connect(self.explorer)
        #建立樹狀圖
        self.tree_view = QTreeView(self)
        self.tree_view.setGeometry(10, 11, 300, 424)
        #隱藏詳細資料標頭
        self.tree_view.setHeaderHidden(True)
        #隱藏水平滾動功能
        self.tree_view.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        # 在樹狀圖中顯示檔案系統的模型
        self.sys_model = QFileSystemModel()
        self.tree_view.setModel(self.sys_model)
        # 啟用樹狀圖的拖曳功能
        self.tree_view.setDragEnabled(True)

    def explorer(self):
        #讓使用者選擇資料夾
        self.folder_path = QFileDialog.getExistingDirectory(self, "選擇資料夾", QDir.rootPath())

        if self.folder_path:
            # 設定根路徑為選擇的資料夾
            self.sys_model.setRootPath(self.folder_path)
            self.tree_view.setRootIndex(self.sys_model.index(self.folder_path))
            # 隱藏不需要的欄位
            for column in range(1, self.sys_model.columnCount()):
                self.tree_view.setColumnHidden(column, True)
            # 設定模型的過濾器，僅顯示資料夾、檔案，只顯示mp3和wav檔案
            self.sys_model.setFilter(QDir.Filter(QDir.Filter.AllDirs | QDir.Filter.NoDotAndDotDot | QDir.Filter.Files))
            self.sys_model.setNameFilters(["*.mp3", "*.wav"])
            self.sys_model.setNameFilterDisables(False)

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = ExplorerBar()
    window.show()
    app.exec()