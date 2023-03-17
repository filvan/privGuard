from src.examples.program.Libretaxi.repository import libretaxi_saveUser
from src.examples.program.Libretaxi.util.util import EscapeMarkdown
from src.examples.program.Libretaxi.locales.english import *

def postToPublicChannel(user):
    text = ""

    if not user['Username']:
        userTextContact = "[" + EscapeMarkdown(user['FirstName']) + " " + EscapeMarkdown(user['LastName']) + "](tg://user?id=" + user['ConsumerID'] + ")"
        text = userTextContact + " has joined LibreTaxi"
    else:
        text = "@" + user['Username'] + " has joined LibreTaxi"

    msgParseMode = ""
    if not user['Username']:
        msgParseMode = "MarkdownV2"

    return user

def run(data_folder, **kwargs):
    print("Init menu")
    user_infos = kwargs.get('extra_args').get('user')
    msg = user_infos['ConsumerID'] + init_menu_welcome

    kwargs.__setitem__("menu_id", "Menu_Ask_Location")
    postToPublicChannel(user_infos)
    return libretaxi_saveUser.run(data_folder, **kwargs)
