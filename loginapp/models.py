from loginapp import db
import bcrypt

# the user table structure 
class DBUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), unique=False, nullable=False)

    def __repr__(self):
        return "<DBUser %r>" % self.username

def setup_db():
    db.create_all()
    user_dict = {
        "admin" : DBUser(username="admin", email="admin@example.com", password=bcrypt.hashpw(b"abc123", bcrypt.gensalt())),
        "guest" : DBUser(username="guest", email="guest@example.com", password=bcrypt.hashpw(b"password", bcrypt.gensalt()))}
    for key, user in user_dict.items():
        print("%s added to the database."% user.username)
        db.session.add(user)
    db.session.commit()