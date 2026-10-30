"""Registration screen. Staff email only, strong password, one account per email."""
import sys
from PySide6.QtWidgets import QApplication, QFrame, QWidget, QLineEdit, QFormLayout, QHBoxLayout, QPushButton, QLabel, QVBoxLayout
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt, Signal
from pathlib import Path
from app.screens.login import LoginScreen 
from app import auth

class RegisterScreen(QWidget):
    joinRequested = Signal()

    def __init__(self, parent=None):
        super(RegisterScreen, self).__init__(parent)
        self.setWindowTitle("Register")
        self.setObjectName("registerScreen")

        PADDING = 32
        FIELD_WIDTH = 300 
        BOX_WIDTH = FIELD_WIDTH + (2 * PADDING)

        # Creating the name input
        self.nameInput = QLineEdit()
        self.nameInput.setObjectName("nameInput")
        self.nameInput.setPlaceholderText("Full name")
        self.nameInput.setMinimumWidth(FIELD_WIDTH)
        self.nameInput.setMaximumWidth(FIELD_WIDTH)

        # Creating email and password inputs
        self.emailInput = QLineEdit()
        self.passwordInput = QLineEdit()
        self.passwordInput.setEchoMode(QLineEdit.EchoMode.Password) # Masks the typed password on screen

        self.emailInput.setObjectName("emailInput")
        self.passwordInput.setObjectName("passwordInput")

        self.passwordInput.setPlaceholderText("Password")
        self.emailInput.setPlaceholderText("@make-it-all.co.uk")
        self.emailInput.setMinimumWidth(FIELD_WIDTH)
        self.passwordInput.setMinimumWidth(FIELD_WIDTH)
        self.emailInput.setMaximumWidth(FIELD_WIDTH)
        self.passwordInput.setMaximumWidth(FIELD_WIDTH)

        self.confirmPasswordInput = QLineEdit()
        self.confirmPasswordInput.setObjectName("confirmPasswordInput")
        self.confirmPasswordInput.setEchoMode(QLineEdit.EchoMode.Password)
        self.confirmPasswordInput.setPlaceholderText("Re-enter password")
        self.confirmPasswordInput.setMinimumWidth(FIELD_WIDTH)
        self.confirmPasswordInput.setMaximumWidth(FIELD_WIDTH)

        # Error message, empty until a check fails
        self.errorLabel = QLabel("")
        self.errorLabel.setObjectName("errorLabel")
        self.errorLabel.setWordWrap(True)

        self.loginLink = QPushButton("Already have an account? Login here")
        self.loginLink.setObjectName("linkButton")                    
        self.loginLink.setFlat(True)                                  # no button background
        self.loginLink.setCursor(Qt.CursorShape.PointingHandCursor)   # hand cursor on hover
        self.loginLink.clicked.connect(self.joinRequested.emit)      

        # Creating the register box and register button
        registerForm = QFormLayout()
        registerBox = QFrame()
        registerBox.setObjectName("registerBox")

        self.registerButton = QPushButton("Register")
        self.registerButton.setObjectName("registerButton")
        self.registerButton.setMinimumWidth(FIELD_WIDTH)
        self.registerButton.setMaximumWidth(FIELD_WIDTH)
        self.registerButton.clicked.connect(self.handleRegister)
        self.nameInput.returnPressed.connect(self.handleRegister)
        self.emailInput.returnPressed.connect(self.handleRegister)
        self.passwordInput.returnPressed.connect(self.handleRegister)
        self.confirmPasswordInput.returnPressed.connect(self.handleRegister)

        # Adding the image
        logoPath = Path(__file__).resolve().parent.parent / "assets" / "Make-it-All-Logo.png"
        logo = QPixmap(str(logoPath)).scaledToWidth(
            BOX_WIDTH, Qt.TransformationMode.SmoothTransformation)
        self.logoLabel = QLabel()
        self.logoLabel.setPixmap(logo)
        self.logoLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Creating the register form box
        registerForm.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.FieldsStayAtSizeHint) # Stops fields growing beyond their size
        registerForm.setRowWrapPolicy(QFormLayout.RowWrapPolicy.WrapAllRows) # Puts each label above its field instead of beside it
        registerForm.setContentsMargins(PADDING, 24, PADDING, PADDING)
        registerForm.addRow("Full name", self.nameInput)
        registerForm.addRow("Email", self.emailInput)
        registerForm.addRow("Password (At least 12 characters)", self.passwordInput)
        registerForm.addRow("Confirm password", self.confirmPasswordInput)
        registerForm.addRow(self.errorLabel)              
        registerForm.addRow(self.registerButton)
        registerForm.addRow(self.loginLink)

        # Styles the inside of the register box
        boxLayout = QVBoxLayout()
        boxLayout.setContentsMargins(0, 0, 0, 0) 
        boxLayout.setSpacing(0)
        boxLayout.addWidget(self.logoLabel)       
        boxLayout.addLayout(registerForm) 
        registerBox.setLayout(boxLayout)

        # Centres the register box
        outer_layout = QHBoxLayout()
        outer_layout.addStretch(1) # Factor 1 so the stretches take all the spare width. With 0, the box gets a third of the window and sits off-centre
        outer_layout.addWidget(registerBox, alignment=Qt.AlignmentFlag.AlignVCenter)
        outer_layout.addStretch(1)               
        self.setLayout(outer_layout)
        
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True) # Sets background colour from styles.qss

    def handleRegister(self):
        name = self.nameInput.text().strip()
        email = self.emailInput.text()
        password = self.passwordInput.text()
        confirm = self.confirmPasswordInput.text()

        #Every field filled in
        if not name or not email.strip() or not password or not confirm:
            self.showError("Please fill in all fields.")
            return

        #Company email
        if not auth.isCompanyEmail(email):
            self.showError("Please use your @make-it-all.co.uk email address.", self.emailInput)
            return

        #One account per email
        if auth.emailExists(email):
            self.showError("An account with this email already exists.", self.emailInput)
            return

        #Strong password (NCSC rules)
        passwordError = auth.checkPassword(password, email)
        if passwordError:
            self.showError(passwordError, self.passwordInput)
            return

        #Passwords match
        if password != confirm:
            self.confirmPasswordInput.clear()
            self.showError("Passwords don't match.", self.confirmPasswordInput)
            return

        # All checks passed: create the account, then go to login
        auth.registerUser(name, email, password)
        self.errorLabel.setText("")
        self.joinRequested.emit()

    def showError(self, message, field=None):
        """Show an error and, if given, put the cursor in the field that needs fixing."""
        self.errorLabel.setText(message)
        if field is not None:
            field.setFocus()



if __name__ == '__main__':

    app = QApplication(sys.argv)
    app.setStyleSheet((Path(__file__).resolve().parent.parent / "styles.qss").read_text())
    # Create and show the form
    window = RegisterScreen()
    window.showMaximized()

    def openLogin():
        window.loginScreen = LoginScreen()   
        window.loginScreen.showMaximized()
        window.hide()

    window.joinRequested.connect(openLogin)

    # Run the main Qt loop
    sys.exit(app.exec())