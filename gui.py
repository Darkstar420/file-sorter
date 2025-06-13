from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout

from mover import move_files
from monitor import start_monitor
from settings import Settings


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.settings = Settings.load()
        self.observer = None
        self.init_ui()

    def init_ui(self):
        self.run_btn = QPushButton("Run Once")
        self.monitor_btn = QPushButton("Enable Monitor")
        layout = QVBoxLayout()
        layout.addWidget(self.run_btn)
        layout.addWidget(self.monitor_btn)
        self.setLayout(layout)

        self.run_btn.clicked.connect(self.run_sorting)
        self.monitor_btn.clicked.connect(self.toggle_monitor)

    def run_sorting(self):
        move_files(self.settings.source, self.settings.rules)

    def toggle_monitor(self):
        if self.observer:
            self.observer.stop()
            self.observer.join()
            self.observer = None
            self.monitor_btn.setText("Enable Monitor")
        else:
            self.observer = start_monitor(self.settings.source, self.settings.rules)
            self.monitor_btn.setText("Disable Monitor")


def launch_gui():
    app = QApplication([])
    w = MainWindow()
    w.show()
    app.exec_()


if __name__ == "__main__":
    launch_gui()
