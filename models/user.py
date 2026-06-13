from pymongo import MongoClient
import bcrypt, jwt, datetime, os

JWT_SECRET = os.environ.get("JWT_SECRET", "PrimeBrawlSuperSecretKey2026")

class UserDB:
    def __init__(self, db):
        self.collection = db.users
    
    def create_user(self, email, password, player_id):
        hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        doc = {"email": email, "password": hashed, "player_id": player_id, "created": datetime.datetime.utcnow()}
        self.collection.insert_one(doc)
        return self.generate_token(player_id)
    
    def verify_login(self, email, password):
        user = self.collection.find_one({"email": email})
        if user and bcrypt.checkpw(password.encode(), user["password"]):
            return self.generate_token(user["player_id"])
        return None
    
    def generate_token(self, player_id):
        return jwt.encode({"player_id": player_id, "exp": datetime.datetime.utcnow() + datetime.timedelta(days=30)}, JWT_SECRET, algorithm="HS256")
