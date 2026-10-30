"""Main window shell: sidebar navigation (filtered by role) and a QStackedWidget that switches between screens."""
 
from PySide6.QtWidgets import QWidget, QStackedWidget, QLabel, QListWidget, QHBoxLayout
 
from app.screens.main_menu import createMenu
 
 
def createMainWindow():
    """Builds the main window and returns it (main.py shows it after login)."""
    window = QWidget()
    window.setObjectName("window")
    window.setWindowTitle("Make-It-All")
    windowLayout = QHBoxLayout()
    window.setLayout(windowLayout)
 
    sidebar = QListWidget()
    sidebar.setObjectName("sidebar")
    sidebar.setFixedWidth(180)
 
    stack = QStackedWidget()
 
    sidebar.addItem("Main Menu")
    stack.addWidget(createMenu())
 
    sidebar.addItem("To-do")
    stack.addWidget(QLabel("To-do page coming soon"))  # placeholder for testing
 
    sidebar.currentRowChanged.connect(stack.setCurrentIndex)
    sidebar.setCurrentRow(0)
 
    windowLayout.addWidget(sidebar)
    windowLayout.addWidget(stack)
 
    window.resize(900, 600)
    return window
 
 
# Test the main window without logging in:  python -m app.main_window
if __name__ == "__main__":
    import sys
    from pathlib import Path
    from PySide6.QtWidgets import QApplication
 
    app = QApplication(sys.argv)
    stylesPath = Path(__file__).resolve().parent / "styles.qss"
    with open(stylesPath) as f:
        app.setStyleSheet(f.read())
 
    window = createMainWindow()
    window.show()
    sys.exit(app.exec())