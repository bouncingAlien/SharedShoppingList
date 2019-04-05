import uuid
from db import db
from werkzeug.security import generate_password_hash, check_password_hash
from models.friendship_requests import FriendshipRequestsModel
from models.items import ItemModel

# friendship many-to-many table
friendship = db.Table("friendship",
                      db.Column("requested_by_public_id", db.String(50), db.ForeignKey("users.user_pid")),
                      db.Column("received_by_public_id", db.String(50), db.ForeignKey("users.user_pid")),
                      )

#items many-to-many table
user_items = db.Table("user_items",
                      db.Column("user_pid", db.String(50), db.ForeignKey("users.user_pid")),
                      db.Column("item_pid", db.String(50), db.ForeignKey("items.item_pid"))
)

class User(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    user_pid = db.Column(db.String(50), unique=True)
    username = db.Column(db.String(16), unique=True)
    email = db.Column(db.String(50), unique=True)
    ps_hash = db.Column(db.String(160))
    friends = db.relationship("User", 
                              secondary=friendship,
                              primaryjoin=(friendship.c.requested_by_public_id == user_pid),
                              secondaryjoin=(friendship.c.received_by_public_id == user_pid),
                              backref=db.backref("friendship", lazy="dynamic"),
                              lazy="dynamic")
    user_requests = db.relationship("FriendshipRequestsModel", backref="users", lazy="dynamic")
    items = db.relationship("ItemModel", secondary="user_items", backref="users", lazy="dynamic")

    def __init__(self, username, email, password):
        self.user_pid = str(uuid.uuid4())
        self.username = username
        self.email = email
        self.ps_hash = User.set_password(password)

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_by_pid(cls, user_pid):
        return cls.query.filter_by(user_pid=user_pid).first()

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def set_password(cls, password):
        return generate_password_hash(password)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def check_password(self, password):
        return check_password_hash(self.ps_hash, password)

    # friendship methods
    def get_friends(self):
        return self.friends.all()

    def get_friend(self, friend_pid):
        return self.friends.filter(friendship.c.received_by_public_id == friend_pid).first()

    def add_friend(self, friend):
        self.friends.append(friend)
        db.session.commit()
        return True

    def delete_friend(self, friend_pid):
        friend = User.find_by_pid(friend_pid)
        self.friends.remove(friend)
        db.session.commit()
        return True
