import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QPushButton)

class ToDoList(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("To-Do List")
        self.resize(500, 450)

        #Style
        self.setStyleSheet(""" QWidget {
                                    background-color: #ffffff;
                                    color: #1e1e1e;
                                    font-family: 'Segoe UI';
                                    font-size: 14px;}
                               QLabel {
                                    color: #555555;
                                    font-size: 13px;}
                               QLineEdit {
                                    background-color: #ffffff;
                                    color: #1e1e1e;
                                    border: 1px solid #000000;
                                    border-radius: 6px;
                                    padding: 8px;}
                               QLineEdit:focus {
                                    border: 2px solid #f5a623;}
                               QPushButton {
                                    background-color: #f5a623;
                                    color: #1e1e1e;
                                    border: 1px solid #000000;
                                    border-radius: 6px;
                                    padding: 8px;}
                               QPushButton:hover {
                                    background-color: #ffb84d;}
                               QPushButton:pressed {
                                    background-color: #d98e12;}
                               QListWidget {
                                    background-color: #ffffff;
                                    color: #1e1e1e;
                                    border: 1px solid #000000;
                                    border-radius: 6px;
                                    padding: 5px;}
                                QListWidget::item:selected {
                                    background-color: transparent;
                                    color: #1e1e1e;}""")


        #Layout Setup
        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        #Heading
        heading = QLabel("To-Do List")
        heading.setStyleSheet("font-size: 24px; font: Segoe UI; font-weight: bold; color: #1e1e1e;")

        #Text input for typing new tasks
        self.taskInput = QLineEdit()
        self.taskInput.setPlaceholderText("Type a new task here...")

        #Adding button
        self.addButton = QPushButton("Add Task")

        #Place input field and button side-by-side using a horizontal layout
        inputLayout = QHBoxLayout()
        inputLayout.addWidget(self.taskInput)
        inputLayout.addWidget(self.addButton)


        #Task list widget to show added tasks
        self.taskList = QListWidget()

        #Add everything to main vertical layout
        layout.addWidget(heading)
        layout.addLayout(inputLayout)
        layout.addWidget(self.taskList)

        self.setLayout(layout)

        #Connecting the buttons
        self.addButton.clicked.connect(self.addTask)
        self.taskInput.returnPressed.connect(self.addTask)

    def addTask(self):

        text = self.taskInput.text().strip()

        if text:
            item = QListWidgetItem(text)
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            item.setCheckState(Qt.Unchecked)
            self.taskList.addItem(item)
            self.taskInput.clear()


# changed as it made 2 qApplication instances which leads to an error.
# Run this file on its own with: python -m app.screens.todo
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = ToDoList()
    window.show()

    sys.exit(app.exec())


