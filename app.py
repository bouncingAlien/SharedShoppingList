from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from flask_cors import CORS
from datetime import datetime, timedelta

from security import authenticate, identity

# resources
from resources.user import UserRegister
from resources.friendship import FriendsList, FriendshipRequest, FriendshipAnswer, GetRequestMessages
from resources.items import ItemsList, Item, ItemShare, ItemImportant, ItemDone

app = Flask(__name__)
CORS(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_EXPIRATION_DELTA"] = timedelta(hours=24)
app.secret_key = "changethis"
api = Api(app)

# db
@app.before_first_request
def create_tables():
    db.create_all()

# login
jwt = JWT(app, authenticate, identity)
# change jwt identity from id to public_id
@jwt.jwt_payload_handler
def make_payload(identity):
    iat = datetime.utcnow()
    exp = iat + app.config.get('JWT_EXPIRATION_DELTA')
    nbf = iat + app.config.get('JWT_NOT_BEFORE_DELTA')
    identity = getattr(identity, 'user_pid') or identity['user_pid']
    return {'exp': exp, 'iat': iat, 'nbf': nbf, 'identity': identity}

# resources
api.add_resource(UserRegister, "/register")
api.add_resource(FriendsList, "/friends")
# all request messages, requests, accepted requests and rejected requests
api.add_resource(GetRequestMessages, "/friendship_messages")
# individual request, to answer
api.add_resource(FriendshipRequest, "/friend/<string:friend_un>")
# to send answer to request
api.add_resource(FriendshipAnswer, "/friendship")
api.add_resource(ItemsList, "/items")
api.add_resource(Item, "/item/<string:item_name>")
api.add_resource(ItemShare, "/item/<string:item_name>/<string:friend_un>")
api.add_resource(ItemImportant, "/item/important/<string:item_name>")
api.add_resource(ItemDone, "/item/done/<string:item_name>")

if __name__ == "__main__":
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)
