def command_decorator(func):
    def func_wrapper(*args, **kwargs):
        bot, update = args
        if update.effective_chat.type != 'group':
            bot.send_message(chat_id=update.message.chat_id, text="This bot is for groups.")
            return
        if update.effective_chat.all_members_are_administrators:
            return func(*args, **kwargs)
        return bot.send_message(chat_id=update.message.chat_id, text="All members of the group must be administrators to use me.")
    return func_wrapper


def get_group_members(chat):
    return [member.user for member in chat.get_administrators()]

def to_tag_str(users):
    return ' '.join([user.mention_markdown() for user in users])
