import os

# Ankerpunkt für die DeerFit Anwendung

class Authenticator:
    
    def __init__(self):
        self.authenticated = False
        self.role = None
        self.mitgliedsnummer = None


    def login(self, mitgliedsnummer, password):
        # Hier könnte noch eine Passwortüberprüfung implementiert werden, z.B. durch Ergänzung der gespeicherten Userdaten um ein Passwort
        if mitgliedsnummer == "admin" and password == "admin":
            self.authenticated = True
            self.role = "Admin"
        else:
            user_data_path = os.path.join(os.path.dirname(__file__), "..", "saves", "user_data", mitgliedsnummer)
            if os.path.isdir(user_data_path):
                self.authenticated = True
                self.role = "User"
                self.mitgliedsnummer = mitgliedsnummer
            else:
                self.authenticated = False
                self.role = None
                
    def logout(self):
        self.authenticated = False
        self.role = None
        self.mitgliedsnummer = None

    

    