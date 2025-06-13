import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QLineEdit, QPushButton, QTableWidget, QTableWidgetItem,
    QHBoxLayout, QLabel, QStatusBar
)
from PyQt5.QtCore import Qt

class FileSorterMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("File Sorter")

        self.rules = []

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout()
        central.setLayout(layout)

        # Source folder
        src_layout = QHBoxLayout()
        src_label = QLabel("Source Folder:")
        self.source_input = QLineEdit()
        src_layout.addWidget(src_label)
        src_layout.addWidget(self.source_input)
        layout.addLayout(src_layout)

        # Rules table
        self.rules_table = QTableWidget(0, 2)
        self.rules_table.setHorizontalHeaderLabels(["Pattern", "Destination"])
        layout.addWidget(self.rules_table)

        # Rule management buttons
        btn_layout = QHBoxLayout()
        add_rule_btn = QPushButton("Add Rule")
        remove_rule_btn = QPushButton("Remove Rule")
        run_btn = QPushButton("Run Once")

        add_rule_btn.clicked.connect(self.add_rule)
        remove_rule_btn.clicked.connect(self.remove_rule)
        run_btn.clicked.connect(self.run_sorting)

        btn_layout.addWidget(add_rule_btn)
        btn_layout.addWidget(remove_rule_btn)
        btn_layout.addWidget(run_btn)
        layout.addLayout(btn_layout)

        self.status = QStatusBar()
        self.setStatusBar(self.status)

    def add_rule(self):
        row_position = self.rules_table.rowCount()
        self.rules_table.insertRow(row_position)
        self.rules_table.setItem(row_position, 0, QTableWidgetItem("*.ext"))
        self.rules_table.setItem(row_position, 1, QTableWidgetItem("D:/Path"))

    def remove_rule(self):
        selected_rows = self.rules_table.selectionModel().selectedRows()
        for row in reversed(selected_rows):
            self.rules_table.removeRow(row.row())

    def run_sorting(self):
        self.rules = []
        for row in range(self.rules_table.rowCount()):
            pattern_item = self.rules_table.item(row, 0)
            dest_item = self.rules_table.item(row, 1)
            if pattern_item and dest_item:
                self.rules.append({
                    "pattern": pattern_item.text(),
                    "dest": dest_item.text()
                })

        source = self.source_input.text()
        if source and self.rules:
            from mover import move_files
            moved_files = move_files(source, self.rules)
            self.status.showMessage(f"Moved {len(moved_files)} files.")
        else:
            self.status.showMessage("Missing source folder or rules.")


def main():
    app = QApplication(sys.argv)
    window = FileSorterMainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
