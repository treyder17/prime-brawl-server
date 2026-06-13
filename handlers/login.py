from protocol.messages import PiranhaMessage
from models.user import UserDB
import json

class LoginMessage(PiranhaMessage):
    def decode(self):
        self.email = self.read_string()
        self.password = self.read_string()
    
    def process(self, session, db):
        token = UserDB(db).verify_login(self.email, self.password)
        if token:
            response = LoginResponseMessage()
            response.token = token
            response.status = 200
            response.message = "Prime ID Login erfolgreich"
            session.send(response)
        else:
            response = LoginFailedMessage()
            response.reason = "Prime ID: Falsche E-Mail oder Passwort"
            session.send(response)

class LoginResponseMessage(PiranhaMessage):
    def encode(self):
        self.write_string(self.token)
        self.write_int(self.status)
        self.write_string(self.message)

class LoginFailedMessage(PiranhaMessage):
    def encode(self):
        self.write_string(self.reason)
