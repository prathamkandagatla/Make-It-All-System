"""Entry point. Run with: python main.py. Creates the QApplication, loads styles.qss and shows the login screen."""
#used to import qss style sheet
import sys
from pathlib import Path
# all the screen imports
from app.screens.login import LoginScreen
from app.screens.register import RegisterScreen
from app.main_window import createMainWindow

from PySide6.QtWidgets import QApplication, QStackedWidget


def main():
    #loads the qss style sheet
    app = QApplication(sys.argv)
    stylesPath = Path(__file__).resolve().parent / "app" / "styles.qss"
    app.setStyleSheet(stylesPath.read_text())

    # loads the login and register screens into a stacked widget so its more fluid to switch between them
    authWindow = QStackedWidget()
    authWindow.setWindowTitle("Make-It-All")
    loginScreen = LoginScreen()
    registerScreen = RegisterScreen()
    authWindow.addWidget(loginScreen)
    authWindow.addWidget(registerScreen)
    # wraps the stacked widget in a function so it can be called only when the button is clicked 
    loginScreen.joinRequested.connect(lambda: authWindow.setCurrentWidget(registerScreen)) 

    registerScreen.joinRequested.connect(lambda: authWindow.setCurrentWidget(loginScreen))

    openWindows = {}
    #function to open the main window after login is successful and close the previous windows
    def openMainWindow(user):
        mainWindow = createMainWindow(user["role"])
        openWindows["main"] = mainWindow
        #formatting choice to follow the log in page style
        mainWindow.showMaximized()
        authWindow.close()
 
    loginScreen.loggedIn.connect(openMainWindow)
 
    authWindow.showMaximized()
    sys.exit(app.exec())
 
 
if __name__ == "__main__":
    main()