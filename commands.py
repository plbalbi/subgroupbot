from telegram import ParseMode
import sqlite3 as lite

from helpers import command_decorator, to_tag_str, get_group_members, get_group_member_keyboard, get_subgroup, insert_subgroup

# CREATE TABLE SubGroup(name TEXT, group_chat_id DOUBLE);
# CREATE TABLE Member(user_id INT, name TEXT, subgroup_chat_id DOUBLE, FOREIGN KEY(subgroup_chat_id) REFERENCES SubGroup(rowid));

@command_decorator
def tag(bot, update):
    bot.send_message(chat_id=update.message.chat_id,
                     text=to_tag_str(get_group_members(update.effective_chat)),
                     parse_mode=ParseMode.MARKDOWN)


@command_decorator
def addsubgroup(bot, update):
    words = update.message.text.split(' ')
    if len(words) == 1:
        return bot.send_message(chat_id=update.message.chat_id, text="You should type the name of the subgroup (\addsubgroup subgroup_name)")
    elif len(words) > 2:
        return bot.send_message(chat_id=update.message.chat_id, text="The subgroup name should be only one word")

    subgroup_name = words[1]

    if len(get_subgroup(update.message.chat_id, subgroup_name)) > 0:
        return bot.send_message(chat_id=update.message.chat_id, text="This subgroup already exists")

    insert_subgroup(subgroup_name, update.message.chat_id)

    bot.send_message(chat_id=update.message.chat_id, text="Adding {}".format(subgroup_name))

@command_decorator
def addmember(bot, update):
    words = update.message.text.split(' ')
    if len(words) == 1:
        return bot.send_message(chat_id=update.message.chat_id, text="You should type the name of the subgroup (\addsubgroup subgroup_name)")
    elif len(words) > 2:
        return bot.send_message(chat_id=update.message.chat_id, text="The subgroup name should be only one word")

    subgroup_name = words[1]

    subgroups = get_subgroup(update.message.chat_id, subgroup_name)
    if len(subgroups) == 0:
        return bot.send_message(chat_id=update.message.chat_id, text='Subgroup does not exist (404)')

    bot.send_message(chat_id=update.message.chat_id,
                     text='Please choose members:',
                     reply_markup=get_group_member_keyboard(update.effective_chat, subgroup_name, update.message.chat_id))


def buttons_callback(bot, update):
    query = update.callback_query
    import pdb; pdb.set_trace()
    data = query.data.split('-')
    # "add_{}_to_{}_{}".format(member.user.id, subgroup_name, group_chat_id)
    if data[0] == "add":
        member_id = data[1]
        subgroup_name = data[3]
        group_chat_id = data[4]


def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id,
                     text="Hello. This bot only works on democratic groups, were everybody is admin.")
