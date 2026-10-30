"""Fake login: checks credentials against data.py, stores the current user and provides role checks -> employee, manager."""
from app.data import USERS

currentMember = None

def signIn(emailInput, passwordInput):
    global currentMember

    for user in USERS:
        if user["email"].strip().lower() == emailInput.strip().lower() and user["password"] == passwordInput:
            currentMember = user
            return currentMember
    return None

def signOut():
    global currentMember
    currentMember = None

def getCurrentMember():
    global currentMember
    return currentMember

EMAIL_DOMAIN = "@make-it-all.co.uk"
MIN_PASSWORD_LENGTH = 12

COMMON_PASSWORDS = {
    "password", "password123", "123456789012", "qwertyuiop",
    "letmein12345", "makeitall123", "iloveyou1234",
}


def isCompanyEmail(email):
    """True if the email ends with the company domain and has a valid part before it."""
    email = email.strip().lower()
    if not email.endswith(EMAIL_DOMAIN):
        return False
    before_EDomain = email[:-len(EMAIL_DOMAIN)]     
    return len(before_EDomain) > 0 and "@" not in before_EDomain and " " not in before_EDomain


def emailExists(email):
    email = email.strip().lower()
    return any(user["email"].lower() == email for user in USERS)


def checkPassword(password, email=""):
    """Return an error message if the password is weak, or None if it's acceptable"""
    if len(password) < MIN_PASSWORD_LENGTH:
        return f"Password must be at least {MIN_PASSWORD_LENGTH} characters."
    if password.lower() in COMMON_PASSWORDS:
        return "That password is too common. Try three random words."
    namePart = email.strip().lower().split("@")[0]
    if len(namePart) >= 3 and namePart in password.lower():
        return "Password shouldn't contain your email name."
    return None


def registerUser(name, email, password):
    """Create a new employee account in memory and return it. Assumes inputs are already validated."""
    newUser = {
        "id": max((user["id"] for user in USERS), default=0) + 1,   # next unused id
        "email": email.strip().lower(),
        "password": password,           
        "name": name.strip(),
        "employeeType": "Employee",     # always Employee: users can't make themselves managers
        "teamIds": [],                  # assigned later by a manager
    }
    USERS.append(newUser)               # in memory only, lasts until the app closes
    return newUser
