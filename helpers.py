# prepare item json for api response
def item_to_json(item):
    created = str(item.time_created).split(" ")
    return {"item_pid": item.item_pid,
            "name": item.name,
            "amount": item.amount,
            "comment": item.comment,
            "important": item.important,
            "done": item.done,
            "created_date": created[0],
            "created_time": created[1]
            }

# prepare friend json for api response
def friend_to_json(friend):
    return {"friend_pid": friend.user_pid,
            "friend_username": friend.username
            }

# prepare message json for api response
def message_to_json(message):
    return {"msg_pid": message.request_pid,
            "msg_from": message.requested_by_pid,
            "msg_status": message.status,
            "msg_text": message.text
            }