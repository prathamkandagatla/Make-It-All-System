"""main menu screen which shows after logging in"""


from PySide6.QtWidgets import QWidget, QFrame, QLabel, QProgressBar, QVBoxLayout
from PySide6.QtCore import Qt
 
from app.data import projects
from app.utils import getPercentage, countDoneTasks, countTasks
 
 

def createMainMenuPage():
    """Builds the main menu (project progress) page and returns it as a widget."""
    page = QWidget()
    layout = QVBoxLayout()
    page.setLayout(layout)
 
 
    header = QVBoxLayout()
    heading = QLabel("Menu")
    
    header.addWidget(heading)
    header.setAlignment(Qt.AlignHCenter)
    layout.addLayout(header)
 
    # - one card per project
    for project in projects:
        projectCard = QFrame()
        projectCard.setObjectName("card")
        projectCardLayout = QVBoxLayout()
        projectCard.setLayout(projectCardLayout)
 
        title = QLabel(project["name"])
        title.setObjectName("cardTitle")
        info = QLabel(f"{countDoneTasks(project)} of {countTasks(project)} tasks done")
        bar = QProgressBar()
        bar.setValue(getPercentage(project))
 
        projectCardLayout.addWidget(title)
        projectCardLayout.addWidget(info)
        projectCardLayout.addWidget(bar)
 
        layout.addWidget(projectCard)
 
    layout.addStretch()
    return page