"""Login screen. Validates against auth.py and opens the main window on success."""
import sys
from PySide6.QtWidgets import QApplication, QFrame, QWidget, QLineEdit, QFormLayout, QHBoxLayout, QPushButton, QLabel, QVBoxLayout
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt, Signal
from pathlib import Path
from app import auth
#from app.screens.register import RegisterScreen # This line should be move to main.py when merged with rest of code

class LoginScreen(QWidget):
    joinRequested = Signal()  
    loggedIn = Signal(dict)  # sends the users data to main when user logs in successfully to pull priorities

    def __init__(self, parent=None):
        super(LoginScreen, self).__init__(parent)
        self.setWindowTitle("Login")
        self.setObjectName("loginScreen")
        self.errorLabel = QLabel("")
        self.errorLabel.setObjectName("errorLabel")   
        self.errorLabel.setWordWrap(True)

        self.joinButton = QPushButton("New Employee? Join here")
        self.joinButton.setObjectName("linkButton")         
        self.joinButton.setFlat(True)                           
        self.joinButton.setCursor(Qt.CursorShape.PointingHandCursor) 
        self.joinButton.clicked.connect(self.joinRequested.emit) 

        PADDING = 32
        FIELD_WIDTH = 300 
        BOX_WIDTH = FIELD_WIDTH + (2 * PADDING)

        # Creating email and password inputs
        self.emailInput = QLineEdit()
        self.passwordInput = QLineEdit()
        self.passwordInput.setEchoMode(QLineEdit.EchoMode.Password) # Masks the typed password on screen

        self.emailInput.setObjectName("emailInput")
        self.passwordInput.setObjectName("passwordInput")

        self.passwordInput.setPlaceholderText("Password")
        self.emailInput.setPlaceholderText("@make-it-all.co.uk")
        self.emailInput.setMinimumWidth(300)
        self.passwordInput.setMinimumWidth(300)
        self.emailInput.setMaximumWidth(300)
        self.passwordInput.setMaximumWidth(300)

        # Creating the login box and log in button
        loginForm = QFormLayout()
        loginBox = QFrame()
        loginBox.setObjectName("loginBox")

        self.loginButton = QPushButton("Log in")
        self.loginButton.setObjectName("loginButton")
        self.loginButton.setMinimumWidth(300)
        self.loginButton.setMaximumWidth(300)
        self.loginButton.clicked.connect(self.handleLogin)
        self.emailInput.returnPressed.connect(self.handleLogin)
        self.passwordInput.returnPressed.connect(self.handleLogin)

        # Adding the image
        logoPath = Path(__file__).resolve().parent.parent / "assets" / "Make-it-All-Logo.png"
        logo = QPixmap(str(logoPath)).scaledToWidth(
            BOX_WIDTH, Qt.TransformationMode.SmoothTransformation)
        self.logoLabel = QLabel()
        self.logoLabel.setPixmap(logo)
        self.logoLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Creating the login form box
        loginForm.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.FieldsStayAtSizeHint) # Stops fields growing beyond their size
        loginForm.setRowWrapPolicy(QFormLayout.RowWrapPolicy.WrapAllRows) # Puts each label above its field instead of beside it
        loginForm.setContentsMargins(PADDING, 24, PADDING, PADDING)
        loginForm.addRow("Email", self.emailInput)
        loginForm.addRow("Password", self.passwordInput)
        loginForm.addRow(self.errorLabel)            
        loginForm.addRow(self.loginButton)
        loginForm.addRow(self.joinButton)

        # Styles the inside of the login box
        boxLayout = QVBoxLayout()
        boxLayout.setContentsMargins(0, 0, 0, 0) 
        boxLayout.setSpacing(0)
        boxLayout.addWidget(self.logoLabel)       
        boxLayout.addLayout(loginForm) 
        loginBox.setLayout(boxLayout)

        # Centres the Login Box
        outer_layout = QHBoxLayout()
        outer_layout.addStretch(1) # Factor 1 so the stretches take all the spare width. With 0, the box gets a third of the window and sits off-centre
        outer_layout.addWidget(loginBox, alignment=Qt.AlignmentFlag.AlignVCenter)
        outer_layout.addStretch(1)               
        self.setLayout(outer_layout)
        
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True) #Sets background colour from styles.qss

    def handleLogin(self):
        email = self.emailInput.text()
        password = self.passwordInput.text()

        if not email.strip() or not password:
            self.errorLabel.setText("Please enter your email and password.")
            return
        
        user = auth.signIn(email, password)

        if user is None:
            self.errorLabel.setText("Incorrect email or password.")
            self.passwordInput.clear()
            self.passwordInput.setFocus()
            return

        self.errorLabel.setText("")
        self.loggedIn.emit(user) #Output for correct Login -> Modify to load the appropriate page according to user role




if __name__ == '__main__':
    from app.screens.register import RegisterScreen #added to test screen without import error
    app = QApplication(sys.argv)
    app.setStyleSheet((Path(__file__).resolve().parent.parent / "styles.qss").read_text())
    # Create and show the form
    window = LoginScreen()
    window.showMaximized()

    def openRegister():
        window.registerScreen = RegisterScreen()  
        window.registerScreen.showMaximized()
        window.hide()

    window.joinRequested.connect(openRegister)
    
    # Run the main Qt loop
    sys.exit(app.exec())