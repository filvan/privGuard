from src.examples.program.libretaxi.repository import libretaxi_saveUser
from src.examples.program.libretaxi.util.util import EscapeMarkdown


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
    locales = kwargs.get('locales')
    user_infos = kwargs.get('extra_args').get('user')
    msg = user_infos['ConsumerID'] + locales.init_menu_welcome

    kwargs.__setitem__("menu_id", "Menu_Ask_Location")
    postToPublicChannel(user_infos)
    return libretaxi_saveUser.run(data_folder, **kwargs)
