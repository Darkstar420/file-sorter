# codex-task: Implement the Qt main window exactly as described in codex-plan.md

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QFileDialog, QTableWidget,
    QTableWidgetItem, QHeaderView, QStatusBar
)
from PySide6.QtCore import Qt
import sys


class FileSorterMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("File Sorter Utility")
        self.setGeometry(100, 100, 800, 600)
        self.init_ui()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout()

        # Source folder picker
        folder_layout = QHBoxLayout()
        self.source_input = QLineEdit()
        browse_button = QPushButton("Browse...")
        browse_button.clicked.connect(self.select_folder)

        folder_layout.addWidget(QLabel("Folder to organize:"))
        folder_layout.addWidget(self.source_input)
        folder_layout.addWidget(browse_button)

        # Rule table
        self.rules_table = QTableWidget(0, 2)
        self.rules_table.setHorizontalHeaderLabels(["File Types", "Destination Folder"])
        self.rules_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # Buttons
        button_layout = QHBoxLayout()
        add_rule_btn = QPushButton("Add Rule")
        remove_rule_btn = QPushButton("Remove Rule")
        run_btn = QPushButton("Run Once")
        monitor_btn = QPushButton("Enable Monitor")

        # For now these buttons do nothing — we'll wire them up later
        button_layout.addWidget(add_rule_btn)
        button_layout.addWidget(remove_rule_btn)
        button_layout.addStretch()
        button_layout.addWidget(run_btn)
        button_layout.addWidget(monitor_btn)

        # Assemble layout
        main_layout.addLayout(folder_layout)
        main_layout.addWidget(QLabel("Sorting Rules:"))
        main_layout.addWidget(self.rules_table)
        main_layout.addLayout(button_layout)

        central_widget.setLayout(main_layout)

        # Status bar
        self.status = QStatusBar()
        self.setStatusBar(self.status)
        self.status.showMessage("Ready")

    def select_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder:
            self.source_input.setText(folder)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FileSorterMainWindow()
    window.show()
    sys.exit(app.exec())
