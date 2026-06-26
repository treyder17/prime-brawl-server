from protocol.messages import PiranhaMessage, MessageID
from models.user import UserDB
import json

class LoginMessage(PiranhaMessage):
    def __init__(self):
        super().__init__()
        self.id = MessageID.LOGIN
    
    def decode(self):
        self.email = self.read_string()
        self.password = self.read_string()
    
    def process(self, db):
        token = UserDB(db).verify_login(self.email, self.password)
        if token:
            return True, token, None
        else:
            return False, None, "Falsche E-Mail oder Passwort"

class LoginResponseMessage(PiranhaMessage):
    def __init__(self, token):
        super().__init__()
        self.id = MessageID.LOGIN_OK
        self.token = token
        self.status = 200
        self.message = "Prime ID Login erfolgreich"
    
    def encode(self):
        self.write_string(self.token)
        self.write_int(self.status)
        self.write_string(self.message)
        return self.payload

class LoginFailedMessage(PiranhaMessage):
    def __init__(self, reason="Prime ID: Falsche E-Mail oder Passwort"):
        super().__init__()
        self.id = MessageID.LOGIN_FAILED
        self.reason = reason
    
    def encode(self):
        self.write_string(self.reason)
        self.write_int(401)
        return self.payload

# ========== KOMPATIBILITÄTSFUNKTIONEN FÜR server.py ==========

def handle_client_hello(data, session):
    """Verarbeitet Client Hello (10100)"""
    print(f"[+] Client Hello von {session}")
    return True

def handle_login(data, session, db):
    """Verarbeitet Login (10101)"""
    msg = LoginMessage()
    msg.decode(data)
    success, token, error = msg.process(db)
    if success:
        return LoginResponseMessage(token)
    else:
        return LoginFailedMessage(error or "Login fehlgeschlagen")
