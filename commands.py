from telegram import ParseMode, ReplyKeyboardRemove
from apifirebase import *

from helpers import command_decorator, to_tag_str, get_group_members, get_group_member_keyboard, get_subgroups_keyboard

@command_decorator
def tag(bot, update):
    words = update.message.text.split(' ')
    if len(words) != 1:
        bot.send_message(chat_id=update.message.chat_id,
                         text='Tag who?',
                         reply_markup=get_subgroups_keyboard(update.effective_chat))

    users = get_members(update.message.chat_id, words[1])
    bot.send_message(chat_id=update.message.chat_id,
                     text=' '.join([user['tag'] for user in users]),
                     parse_mode=ParseMode.MARKDOWN)


@command_decorator
def addsubgroup(bot, update):
    words = update.message.text.split(' ')
    if len(words) == 1:
        return bot.send_message(chat_id=update.message.chat_id, text="You should type the name of the subgroup (\addsubgroup subgroup_name)")
    elif len(words) > 2:
        return bot.send_message(chat_id=update.message.chat_id, text="The subgroup name should be only one word")

    subgroup_name = words[1]

    subgroup = get_subgroup(update.message.chat_id, subgroup_name)
    if subgroup and len(subgroup) > 0:
        return bot.send_message(chat_id=update.message.chat_id, text="This subgroup already exists")

    add_subgroup(update.message.chat_id, subgroup_name)

    bot.send_message(chat_id=update.message.chat_id, text="Adding {}".format(subgroup_name))

@command_decorator
def addmember(bot, update):
    words = update.message.text.split(' ')
    if len(words) == 1:
        return bot.send_message(chat_id=update.message.chat_id, text="You should type the name of the subgroup (\addsubgroup subgroup_name)")
    elif len(words) > 2:
        return bot.send_message(chat_id=update.message.chat_id, text="The subgroup name should be only one word")

    subgroup_name = words[1]

    subgroup = get_subgroup(update.message.chat_id, subgroup_name)
    if subgroup is None:
        return bot.send_message(chat_id=update.message.chat_id, text='Subgroup does not exist (404)')

    bot.send_message(chat_id=update.message.chat_id,
                     text='Please choose members:',
                     reply_markup=get_group_member_keyboard(update.effective_chat, subgroup_name))


def buttons_callback(bot, update):
    query = update.callback_query
    data = query.data.split('_')
    # "add_{}_to_{}_{}".format(member.user.id, subgroup_name, group_chat_id)
    ReplyKeyboardRemove(remove_keyboard=True)
    if data[0] == "add":
        member_id = data[1]
        user = update.effective_chat.get_member(member_id).user
        if not is_member(data[4], data[3], user.id):
            # import pdb; pdb.set_trace()
            add_member(data[4], data[3], user.id, user.username, user.mention_markdown())
            bot.send_message(chat_id=update.effective_chat.id, text="OK. {} agregado".format(user.username))
        else:
            bot.send_message(chat_id=update.effective_chat.id, text="Ya estaba este")
    elif data[0] == "tag":
        users = get_members(update.effective_chat.id, data[1])
        bot.send_message(chat_id=update.effective_chat.id,
                         text=' '.join([user['tag'] for user in users]),
                         parse_mode=ParseMode.MARKDOWN)


@command_decorator
def subgroups(bot, update):
    subgroups = [subgroup["tag"] for subgroup in get_subgroups(update.effective_chat.id)]
    bot.send_message(chat_id=update.effective_chat.id, text="\n".join(subgroups))
    bot.send_message(chat_id=update.effective_chat.id, text="To get the members of a group use /members <subgroup_name>")

@command_decorator
def members(bot, update):
    words = update.message.text.split(' ')
    if len(words) == 1:
        return bot.send_message(chat_id=update.message.chat_id, text="You should type the name of the subgroup (/members subgroup_name)")
    elif len(words) > 2:
        return bot.send_message(chat_id=update.message.chat_id, text="The subgroup name should be only one word")

    subgroup_name = words[1]

    subgroup = get_subgroup(update.message.chat_id, subgroup_name)
    if subgroup is None:
        return bot.send_message(chat_id=update.message.chat_id, text='Subgroup does not exist (404)')

    members = [member["username"] for member in get_members(update.effective_chat.id, subgroup_name)]
    bot.send_message(chat_id=update.effective_chat.id, text="\n".join(members))



def start(bot, update):
    add_group(update.effective_chat.id, update.effective_chat.title)
    bot.send_message(chat_id=update.effective_chat.id,
                     text="Hello. This bot only works on democratic groups, were everybody is admin.")
