from flask_restful import Resource, reqparse
from flask_jwt import jwt_required, current_identity
import json
from models.user import User
from models.items import ItemModel
from helpers import item_to_json

class ItemsList(Resource):

    @jwt_required()
    def get(self):
        user = User.find_by_username(current_identity.username)
        result = ItemModel.get_all_items(user)
        return {"items": [item_to_json(i) for i in result]}

class Item(Resource):

    @jwt_required()
    def get(self, item_name):
        user = User.find_by_username(current_identity.username)
        item = ItemModel.find_item_by_name(user,item_name)
        print(item.is_shared_with())
        if item:
            return item_to_json(item)
        else:
            return {"message": "Item not found!"}, 401

    @jwt_required()
    def post(self, item_name):
        parser = reqparse.RequestParser()
        parser.add_argument("amount",
                          type=str,
                          required=False
                          )
        parser.add_argument("comment",
                          type=str,
                          required=False
                          )
        data = parser.parse_args()
        user = User.find_by_username(current_identity.username)
        try:
            item = ItemModel.create_item(item_name, data["amount"], data["comment"], user.username)
            item.add_item(user)
            return {"item": item_to_json(item)}
        except:
            return {"message": "item not created. Internal server error"}, 500

    @jwt_required()
    def delete(self, item_name):
        user = User.find_by_username(current_identity.username)
        item = ItemModel.find_item_by_name(user,item_name)
        if item:
            try:
                item.delete_item(user)
                return {"message": "Item deleted"}, 201
            except:
                return {"message": "Item not deleted. Internal server error"}, 501
        else:
            return {"message": "Item not found"}

    @jwt_required()
    def put(self, item_name):
        parser = reqparse.RequestParser()
        parser.add_argument("amount",
                          type=str,
                          required=False
                          )
        parser.add_argument("comment",
                          type=str,
                          required=False
                          )
        data = parser.parse_args()
        amount = None
        comment = None
        if data["amount"]:
            amount = data["amount"]
        if data["comment"]:
            comment = data["comment"]
        user = User.find_by_username(current_identity.username)
        item = ItemModel.find_item_by_name(user, item_name)
        if item:
            try:
                item.edit_item(amount, comment)
                return {"message": item.name}, 201
            except:
                return {"message": "Item not changed. Internal server error."}, 501
        else:
            item = ItemModel.create_item(item_name, data["amount"], data["comment"])
            item.add_item(user)
            return {"message": "item created"}, 201

class ItemShare(Resource):

    @jwt_required()
    def post(self, item_name, friend_un):
        user = User.find_by_username(current_identity.username)
        friend = User.find_by_username(friend_un)
        item = ItemModel.find_item_by_name(user, item_name)
        try:
            item.add_item(friend)
            return {"message": "Item shared"}, 201
        except:
            return {"message": "Item not shared. Internal server error"}, 500

    @jwt_required()
    def delete(self, friend_un, item_name):
        user = User.find_by_username(current_identity.username)
        friend = User.find_by_username(friend_un)
        item = ItemModel.find_item_by_name(item_name)
        if item and item.owner == user.username:
            try:
                item.delete_item(friend_un)
                return {"message": "Item deleted from share"}, 201
            except:
                return {"message": "Item not deleted from share. Internal server error"}, 500

class ItemImportant(Resource):

    @jwt_required()
    def post(self, item_name):
        user = User.find_by_username(current_identity.username)
        item = ItemModel.find_item_by_name(user, item_name)
        if item:
            try:
                item.is_important()
                return {"message": "Item set as important!"}, 201
            except:
                return {"message": "Item not changed. Internal server error."}, 500
        else:
            return {"message": "Item not found!"}

    @jwt_required()
    def delete(self, item_name):
        user = User.find_by_username(current_identity.username)
        item = ItemModel.find_item_by_name(user, item_name)
        if item:
            try:
                item.is_not_important()
                return {"message": "Item set as not important"}, 201
            except:
                return {"message": "Item not changed. Internal server error."}, 500
        else:
            {"message": "Item not found!"}
        
class ItemDone(Resource):

    @jwt_required()
    def post(self, item_name):
        user = User.find_by_username(current_identity.username)
        item = ItemModel.find_item_by_name(user, item_name)
        if item:
            try:
                item.is_done()
                return {"message": "Item set as done!"}, 201
            except:
                return {"message": "Item not changed. Internal server error."}, 500
        else:
            return {"message": "Item not found!"}

    @jwt_required()
    def delete(self, item_name):
        user = User.find_by_username(current_identity.username)
        item = ItemModel.find_item_by_name(user, item_name)
        if item:
            try:
                item.is_not_done()
                return {"message": "Item set as not done"}, 201
            except:
                return {"message": "Item not changed. Internal server error."}, 500
        else:
            {"message": "Item not found!"}