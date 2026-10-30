"""Main window shell: sidebar navigation (filtered by role) and a QStackedWidget that switches between screens."""


from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QTreeWidget, QTreeWidgetItem, QStackedWidget, QLabel
from pathlib import Path

from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt

from app.screens.main_menu import createMainMenuPage

assetsDir = Path(__file__).resolve().parent / "assets"


def createPlaceholderPage(name):
    """Temporary page until all screens are ready."""

    return QLabel(f"{name} page coming soon")

#temporary test drop down
Dropdown = ("information", [
    ("technical", lambda: createPlaceholderPage("technical")),
    ("non-technical", lambda: createPlaceholderPage("non-technical")),
])

#edits drop down for both manager and employee roles
pagesByRole = {
    "Manager": [
        ("Home", createMainMenuPage),
        ("Dashboard", lambda: createPlaceholderPage("Dashboard")),
        ("To-do", lambda: createPlaceholderPage("To-do")),
        ("Project-To-do", lambda: createPlaceholderPage("To-do, can add tasks to project")),
        Dropdown,
    ],
    "Employee": [
        ("Home", createMainMenuPage),
        ("To-do", lambda: createPlaceholderPage("To-do")),
        ("Topics", lambda: createPlaceholderPage("Topics")),
        Dropdown,
    ],
}
 
 
def addPage(stack, item, createPage):
    """Builds a page, adds it to the stack, and remembers its stack position on the sidebar item."""
    pageIndex = stack.addWidget(createPage())  # addWidget returns the new page's position
    item.setData(0, Qt.UserRole, pageIndex)
 
 
def createSidebarLogo():
    """Builds the logo shown at the top of the sidebar."""
    logo = QLabel()
    logo.setObjectName("sidebarLogo")
    logo.setAlignment(Qt.AlignCenter)
    pixmap = QPixmap(str(assetsDir / "Make-It-All-logo.png"))
    if pixmap.isNull():
        logo.setText("Make-It-All")  # fallback if the logo file does not load or is missing
    else:
        logo.setPixmap(pixmap.scaledToWidth(160, Qt.SmoothTransformation))
    return logo
 
 #builds main window with sidebar and saves as a page

def createMainWindow(role):
    window = QWidget()
    window.setObjectName("window")
    window.setWindowTitle("Make-It-All")
    windowLayout = QHBoxLayout()
    window.setLayout(windowLayout)
 
    # - sidebar: a container with the logo on top and the navigation underneath
    sidebar = QWidget()
    sidebar.setObjectName("sidebar")
    sidebar.setAttribute(Qt.WA_StyledBackground, True)  # lets styles.qss give it a background colour
    sidebar.setFixedWidth(200)
    sidebarLayout = QVBoxLayout()
    sidebar.setLayout(sidebarLayout)
 
    sidebarLayout.addWidget(createSidebarLogo())
 
    navTree = QTreeWidget()  # like a list, but items can have items inside them (dropdowns)
    navTree.setObjectName("navTree")
    navTree.setHeaderHidden(True)
    sidebarLayout.addWidget(navTree)
 
    stack = QStackedWidget()
 
    # - add each page this role can see
    for pageName, target in pagesByRole[role]:
        item = QTreeWidgetItem([pageName])
        navTree.addTopLevelItem(item)
 
        if isinstance(target, list):
            # a dropdown: add each page inside it as a child item
            for childName, createPage in target:
                childItem = QTreeWidgetItem([childName])
                item.addChild(childItem)
                addPage(stack, childItem, createPage)
        else:
            addPage(stack, item, target)
 
    # - what happens when a sidebar item is clicked
    def onItemClicked(item, column):
        pageIndex = item.data(0, Qt.UserRole)
        if pageIndex is None:
            # a dropdown heading has no page of its own, so open or close it instead
            item.setExpanded(not item.isExpanded())
        else:
            stack.setCurrentIndex(pageIndex)
 
    navTree.itemClicked.connect(onItemClicked)
    navTree.setCurrentItem(navTree.topLevelItem(0))  # highlight Home at the start
    stack.setCurrentIndex(0)
 
    windowLayout.addWidget(sidebar)
    windowLayout.addWidget(stack)
 
    window.resize(900, 600)
    return window
 
 
# Test - python -m app.main_window
if __name__ == "__main__":
    import sys
    from PySide6.QtWidgets import QApplication
 
    app = QApplication(sys.argv)
    stylesPath = Path(__file__).resolve().parent / "styles.qss"
    with open(stylesPath) as f:
        app.setStyleSheet(f.read())
 
    window = createMainWindow("Manager")
    window.show()
    sys.exit(app.exec())