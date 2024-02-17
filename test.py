from PySide6.QtWidgets import QApplication,QMainWindow,QWidget
from YtbDownloader_ui import Downloader
class MyApp(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.downloader = Downloader()
        self.downloader.setupUi(self)
if __name__ == '__main__':
    app = QApplication([])
    window = MyApp()
    window.show()
    app.exec()