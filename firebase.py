from firebase import firebase

app = firebase.FirebaseApplication('https://subgroupsbot.firebaseio.com/', None)


def subgroups():
    return app.get('/subgroups', None).values()


def add_subgroup(tag, chat_id):
    subgroup = {
        'tag': tag,
        'chat_id': chat_id,
        'members': None
    }
    return app.post('/subgroups', subgroup)

def get_subgroup(tag, chat_id):
    return app.get('/subgroups', None, params={'tag': tag, 'chat_id': chat_id})

def add_member(subgroup_id, user_id, username, tag):
    member = {
        'user_id': user_id,
        'username': username,
        'tag': tag
    }
    return app.post('/subgroups/{}/members'.format(subgroup_id), member)
