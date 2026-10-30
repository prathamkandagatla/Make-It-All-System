import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QListWidget,
    QListWidgetItem)

class TeamToDoList(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Team Project To-Do List")
        self.resize(500, 450)

        #Style
        self.setStyleSheet(""" QWidget {
                                    background-color: #ffffff;
                                    color: #1e1e1e;
                                    font-family: 'Segoe UI';
                                    font-size: 14px;}
                               QLabel {
                                    color: #555555;
                                    font-size: 13px}
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
        heading = QLabel("Team Project To-do List")
        heading.setStyleSheet("font-size: 24px; font: Segoe UI; font-weight: bold; color: #1e1e1e;")

        #Task list pre-populated with tasks
        self.taskList = QListWidget()

        #Pre-populating tasks (Testing)
        managerTasks = [
                "task 1",
                "task 2",
                "task 3",
                "task 4"]

        for taskText in managerTasks:
            item = QListWidgetItem(taskText)
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            item.setCheckState(Qt.Unchecked)
            self.taskList.addItem(item)

        #Add everything to main vertical layout
        layout.addWidget(heading)
        layout.addWidget(self.taskList)

        self.setLayout(layout)


app = QApplication(sys.argv)
app.setStyle("Fusion")
window = TeamToDoList()
window.show()

sys.exit(app.exec())


