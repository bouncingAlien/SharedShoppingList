from db import db
from sqlalchemy import func
import uuid

class ItemModel(db.Model):

    __tablename__ = "items"

    id = db.Column(db.Integer, primary_key=True)
    item_pid = db.Column(db.String, unique=True)
    name = db.Column(db.String(40))
    amount = db.Column(db.String(20))
    comment = db.Column(db.String(150))
    owner = db.Column(db.String(50))
    important = db.Column(db.Boolean, default=False)
    done = db.Column(db.Boolean, default=False)
    time_created = db.Column(db.DateTime(timezone=True), server_default=func.now())
    time_updated = db.Column(db.DateTime(timezone=True), onupdate=func.now())

    def __init__(self, name, amount, comment, owner):
        self.item_pid = str(uuid.uuid4())
        self.name = name
        self.amount = amount
        self.comment = comment
        self.owner = owner

    @classmethod
    def create_item(cls, name, amount, comment, owner):
        return cls(name, amount, comment, owner)

    @classmethod
    def get_all_items(cls, user):
        return user.items.all()

    @classmethod
    def find_item_by_name(cls, user, item_name):
        return user.items.filter_by(name=item_name).first()

    @classmethod
    def find_item_by_pid(cls, user, item_pid):
        return user.items.filter_by(item_pid=item_pid).first()

    def add_item(self, user):
        user.items.append(self)
        db.session.commit()
        return True

    def delete_item(self, user):
        user.items.remove(self)
        db.session.commit()
        return True

    def edit_item(self, amount, comment):
        if amount:
            self.amount = amount
        if comment:
            self.comment = comment
        db.session.commit()
        return True

    # edit "important" value
    def is_important(self):
        self.important = True
        db.session.commit()
        return True

    def is_not_important(self):
        self.important = False
        db.session.commit()
        return True

    # edit "done" value
    def is_done(self):
        self.done = True
        db.session.commit()
        return True

    def is_not_done(self):
        self.done = False
        db.session.commit()
        return True

    # get shared users
    def is_shared_with(self):
        return self.users