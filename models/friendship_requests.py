from db import db
import uuid

class FriendshipRequestsModel(db.Model):

    __tablename__ = "requests"

    id = db.Column(db.Integer, primary_key=True)
    request_pid = db.Column(db.String(50), unique=True)
    requested_to = db.Column(db.String(50), db.ForeignKey("users.user_pid"))
    requested_by_pid = db.Column(db.String(50))
    text = db.Column(db.String(100))
    # 0 - pending, 1 - read,  2 - rejected, 3 - accepted
    status = db.Column(db.Integer)

    def __init__(self, requested_to, requested_by_public_id, text, status):
        self.request_pid = str(uuid.uuid4())
        self.requested_to = requested_to
        self.requested_by_pid = requested_by_public_id
        self.text = text
        self.status = status

    @classmethod
    def create_message(cls, requested_to, requested_by, text, status):
        return cls(requested_to, requested_by, text, status)

    # find message by public id
    @classmethod
    def find_by_pid(cls, request_pid):
        return cls.query.filter_by(request_pid=request_pid).first()

    # send new friendship request
    @classmethod
    def send_request(cls, user, friend):
        text = "{} wants to be your friend!".format(user.username)
        new_request = FriendshipRequestsModel.create_message(friend.user_pid, user.user_pid, text, 0)
        new_request.commit_message()
        return True

    # send answer to request
    @classmethod
    def send_answer(cls, requested_to, requested_by, accepted):
        if accepted:
            text = "{} accepted your request for friendship.".format(requested_by.username)
            answer = cls.create_message(requested_to.user_pid, requested_to.user_pid, text, 3)
        else:
            text = "{} rejected your request for friendship.".format(requested_by.username)
            answer = cls.create_message(requested_to.user_pid, requested_to.user_pid, text, 2)
        answer.commit_message()
             
    @classmethod
    def get_all_requests(self, user):
        return user.user_requests.all()

    def commit_message(self):
        db.session.add(self)
        db.session.commit()

    # accept request and create answer
    def accept_request(self, requested_by, requested_to):
        self.status = 3
        requested_by.add_friend(requested_to)
        requested_to.add_friend(requested_by)
        answer = FriendshipRequestsModel.send_answer(requested_to, requested_by, True)
        return True

    # reject request and create answer
    def reject_request(self, requested_by, requested_to):
        self.status = 2
        answer = FriendshipRequestsModel.send_answer(requested_to, requested_by, False)
        return True
