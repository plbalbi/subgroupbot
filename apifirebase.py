from firebase import firebase

app = firebase.FirebaseApplication('https://subgroupsbot.firebaseio.com/', None)

############################ GROUPS ############################

def groups():
    try:
        return list(app.get('/groups', None).values())
    except AttributeError:
        return []

def add_group(chat_id, group_name):
    group = {
        'chat_id': chat_id,
        'group_name': group_name
    }
    return app.put('/groups/', chat_id, group)

def get_group(chat_id):
    return app.get('/groups', chat_id)

def delete_group(chat_id):
    return app.delete('/groups', chat_id)


########################## SUBGROUPS ###########################

def subgroups(chat_id):
    try:
        return list(app.get('/groups/{}/subgroups'.format(chat_id), None).values())
    except AttributeError:
        return []

def add_subgroup(chat_id, tag):
    subgroup = {
        'tag': tag
    }
    return app.put('/groups/{}/subgroups'.format(chat_id), tag, subgroup)

def get_subgroup(chat_id, tag):
    return app.get('/groups/{}/subgroups'.format(chat_id), tag)

def delete_group(chat_id, tag):
    return app.delete('/groups/{}/subgroups'.format(chat_id), tag)

########################### MEMBERS ############################

def members(chat_id, tag):
    try:
        return list(app.get('/groups/{}/subgroups/{}/members'.format(chat_id, tag), None).values())
    except AttributeError:
        return []

def add_member(chat_id, tag, user_id, username, usertag):
    member = {
        'user_id': user_id,
        'username': username,
        'tag': usertag
    }
    return app.post('/groups/{}/subgroups/{}/members'.format(chat_id, tag), member)
