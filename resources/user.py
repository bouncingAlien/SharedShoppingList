from flask_restful import Resource, reqparse
from models.user import User

class UserRegister(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument("username",
        type=str,
        required=True,
        help="This filed cannot be blank"
    )
    parser.add_argument("password",
        type=str,
        required=True,
        help="This filed cannot be blank"
    )
    parser.add_argument("email",
        type=str,
        required=True,
        help="This filed cannot be blank"
    )

    def post(self):
        data = UserRegister.parser.parse_args()

        # check is username or email taken
        if User.find_by_username(data["username"]):
            return {"Message": "Username is already taken."},  400
        elif User.find_by_email(data["email"]):
            return {"Message": "Email address is already taken."}, 400

        # if not, create new user
        user = User(data["username"], data["email"], data["password"])
        user.save_to_db()

        return {"Message": "User created"}, 201