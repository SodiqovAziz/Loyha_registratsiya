import sys
import json
import os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIntValidator


class RegistrationWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Registration")
        self.init_ui()

    def init_ui(self):
        self.vbox = QVBoxLayout()
        self.hbox = QHBoxLayout()

        self.b1 = QLabel("Name: ")
        self.b2 = QLineEdit("")
        self.hbox.addWidget(self.b1)
        self.hbox.addWidget(self.b2)

        self.b3 = QLabel("Age: ")
        self.b4 = QLineEdit("")
        self.b4.setValidator(QIntValidator(1, 99, self))
        self.hbox1 = QHBoxLayout()
        self.hbox1.addWidget(self.b3)
        self.hbox1.addWidget(self.b4)

        self.b5 = QLabel("Login: ")
        self.b6 = QLineEdit("")
        self.hbox2 = QHBoxLayout()
        self.hbox2.addWidget(self.b5)
        self.hbox2.addWidget(self.b6)

        self.b7 = QLabel("Password: ")
        self.b8 = QLineEdit("")
        self.b8.setEchoMode(QLineEdit.Password)
        self.hbox3 = QHBoxLayout()
        self.hbox3.addWidget(self.b7)
        self.hbox3.addWidget(self.b8)

        self.vbox.addLayout(self.hbox)
        self.vbox.addLayout(self.hbox1)
        self.vbox.addLayout(self.hbox2)
        self.vbox.addLayout(self.hbox3)

        self.save_button = QPushButton("Registratsiya")
        self.save_button.clicked.connect(self.on_register)
        self.vbox.addWidget(self.save_button)

        self.setLayout(self.vbox)
        self.show()

    def save_to_json(self, name, age, login, password):
        data = {"Name": name, "Age": age, "Login": login, "Password": password}

        if os.path.exists('registration_data.json'):
            with open('registration_data.json', 'r') as file:
                try:
                    existing_data = json.load(file)
                except json.JSONDecodeError:
                    existing_data = {"obyectlar": []}
        else:
            existing_data = {"obyectlar": []}

        existing_data["obyectlar"].append(data)

        with open('registration_data.json', 'w') as file:
            json.dump(existing_data, file, indent=4)

    def validate_name(self, name):
        if not name:
            return "Name cannot be empty."
        if not name.isalpha():
            return "Name should only contain alphabetic characters."
        return None

    def validate_age(self, age):
        if not age:
            return "Age cannot be empty."

    def validate_login(self, login):
        if not login:
            return "Login cannot be empty."
        if self.is_login_existing(login):
            return f"Login '{login}' is already taken. Please choose a different login."
        return None

    def validate_password(self, password):
        if len(password) < 6:
            return "Password must be at least 6 characters long."
        if not any(char.isdigit() for char in password):
            return "Password must contain at least one number."
        if not any(char in "!@#$%^&*()_+-=<>?/;:" for char in password):
            return "Password must contain at least one special character."
        return None

    def is_login_existing(self, login):
        if os.path.exists('registration_data.json'):
            with open('registration_data.json', 'r') as file:
                try:
                    data = json.load(file)
                except json.JSONDecodeError:
                    data = {"users": []}
                if "users" in data:
                    for user in data["users"]:
                        if user["Login"] == login:
                            return True
        return False

    def on_register(self):
        name = self.b2.text()
        age = self.b4.text()
        login = self.b6.text()
        password = self.b8.text()

        name_error = self.validate_name(name)
        age_error = self.validate_age(age)
        login_error = self.validate_login(login)
        password_error = self.validate_password(password)

        if name_error:
            QMessageBox.warning(self, "Validation Error", name_error)
            return
        if age_error:
            QMessageBox.warning(self, "Validation Error", age_error)
            return
        if login_error:
            new_login, ok = QInputDialog.getText(self, "Login Already Exists", login_error + "\nEnter a new login:")
            if ok and new_login:
                self.b6.setText(new_login)
                return
            else:
                return
        if password_error:
            QMessageBox.warning(self, "Validation Error", password_error)
            return

        self.save_to_json(name, age, login, password)
        QMessageBox.information(self, "Registration", "Registration successful! Data saved to JSON.")


def main():
    app = QApplication(sys.argv)
    win = RegistrationWindow()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()