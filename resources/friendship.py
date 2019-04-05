from flask_restful import Resource, reqparse
from flask_jwt import jwt_required, current_identity
from models.user import User
from models.friendship_requests import FriendshipRequestsModel
from helpers import friend_to_json, message_to_json

class FriendsList(Resource):

    @jwt_required()
    def get(self):
        user = User.find_by_username(current_identity.username)
        result = user.get_friends()
        if result == "NoneType":
            return {}
        return {"friends": [friend_to_json(f) for f in result]}

class Friend(Resource):

    # get individual friend, exmp. for item sharing
    @jwt_required()
    def get(self, friend_pid):
        user = User.find_by_username(current_identity.username)
        return friend_to_json(user.get_friend(friend_pid))

    # delete individual friend
    @jwt_required()
    def delete(self, friend_pid):
        user = User.find_by_username(current_identity.username)
        try:
            user.delete_friend(friend_pid)
            return {"message": "friend deleted"}, 201
        except:
            return {"message": "Friend not deleted. Internal server error."}, 501

class GetRequestMessages(Resource):

    # get all request messages
    @jwt_required()
    def get(self):
        user = User.find_by_username(current_identity.username)
        messages = FriendshipRequestsModel.get_all_requests(user)
        return {"messages": [message_to_json(m) for m in messages]}

class FriendshipRequest(Resource): 

    # send friednship request
    @jwt_required()
    def post(self, friend_un):
        user = User.find_by_username(current_identity.username)
        friend = User.find_by_username(friend_un)
        if friend:
            try:
                FriendshipRequestsModel.send_request(user, friend)
                return {"message": "Request sent."}, 201
            except:
                return {"message": "Request not sent. Internal server error."}, 500
        return {"message": "User not found!"}

class FriendshipAnswer(Resource):

    # send answer to friendship request
    @jwt_required()
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("action",
                           type=str,
                           required=True,
                           help="Provide answer, do you accept or decline friendship"
                           )
        parser.add_argument("request_pid",
                           type=str,
                           required=True,
                           help="Request ID is missing."
                           )
        data = parser.parse_args()
        # indentify current user
        user = User.find_by_username(current_identity.username)
        # get request
        request = FriendshipRequestsModel.find_by_pid(data["request_pid"])
        # get user who have sent request
        friend = User.find_by_pid(request.requested_by_pid)
        if data["action"] == "accept":
            try:
                request.accept_request(friend, user)
                return {"message": "Friend added"}, 201
            except:
                return {"message": "Server error. Friend not added!"}, 500
        elif data["action"] == "decline":
            try:
                request.decline_request(friend, user)
                return {"message": "Friendship decliend."}, 201
            except:
                return {"message": "Server error. Friendship status unanswerd!"}, 500
        