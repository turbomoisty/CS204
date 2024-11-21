from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, user_id, username, email):
        self.id = user_id 
        self.username = username
        self.email = email

    @staticmethod
    def from_db_row(row):
        return User(user_id=row['id'], username=row['username'], email=row['email'])