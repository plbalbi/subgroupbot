from telegram import InlineKeyboardButton, InlineKeyboardMarkup

import sqlite3 as lite

def command_decorator(func):
    def func_wrapper(*args, **kwargs):
        bot, update = args
        if update.effective_chat.type != 'group':
            bot.send_message(chat_id=update.message.chat_id,
                             text="This bot is for groups.")
            return
        # if update.effective_chat.all_members_are_administrators:
        return func(*args, **kwargs)
        # return bot.send_message(chat_id=update.message.chat_id,
                                # text="All members of the group must be administrators to use me.")
    return func_wrapper


def get_group_members(chat):
    return [member.user for member in chat.get_administrators()]


def get_group_member_keyboard(chat, subgroup_name):
    group_chat_id = chat.id
    keys = [InlineKeyboardButton(member.user.username or member.user.name,
                                     callback_data="add_{}_to_{}_{}".format(member.user.id, subgroup_name, group_chat_id))
                for member in chat.get_administrators()]
    keyboard = []
    keyboard_row = []
    for i in range(len(keys)):
        keyboard_row.append(keys[i])
        if i % 3 == 2:
            keyboard.append(keyboard_row)
            keyboard_row = []
    if len(keyboard_row) > 0:
        keyboard.append(keyboard_row)
    return InlineKeyboardMarkup(keyboard)


def to_tag_str(users):
    return ' '.join([user.mention_markdown() for user in users])
