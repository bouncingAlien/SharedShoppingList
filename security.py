from models.user import User

def authenticate(username, password):
    user = User.find_by_username(username)
    # check does user exists
    if user is None:
        return {"Message": "Username not found."}, 401

    # check password
    if user.check_password(password):
        return user
    else:
         return {"Message": "Username and password do not match"}, 401

def identity(payload):
    user_pid = payload["identity"]
    return User.find_by_pid(user_pid)