from src.examples.program.libretaxi.menu import libretaxi_init_menu_handler, libretaxi_ask_location_menu_handler, \
    libretaxi_feed_menu_handler, \
    libretaxi_post_menu_handler
from src.examples.program.libretaxi.repository import libretaxi_findUser, libretaxi_saveUser


def isStateChanged(data_folder, **kwargs):
    user = libretaxi_findUser.run(data_folder, **kwargs)
    previousState = kwargs.get('prev_state')
    if not user:
        return True
    return user.MenuID != previousState


def oneTimeMessages(user, locales):
    msg = user.DataSubjectID + locales.main_welcome_link
    return user


def run(data_folder, **kwargs):
    pd = kwargs.get('pandas')
    locales = kwargs.get('locales')
    text = kwargs.get('extra_args').get('text')
    extra_args = kwargs.get('extra_args')
    # set for this code a true previous state
    libretaxi_users = pd.read_csv(data_folder + "users/data.csv")
    last_user = libretaxi_users.iloc[-1:]
    kwargs.__setitem__("prev_state", True)
    user = libretaxi_findUser.run(data_folder, **kwargs)
    if not user:
        DataSubjectID = last_user.DataSubjectID
        MenuID = "Menu_Init"
        ReportCnt = 0
        ShadowBanned = False
        extra_args.__setitem__("user_id", DataSubjectID)
        extra_args.__setitem__("menu_txt", MenuID)
        extra_args.__setitem__("shadow_banned", ShadowBanned)
        extra_args.__setitem__("reportCnt", ReportCnt)
    else:
        MenuID = str(user.MenuID)
    # save user
    kwargs.__setitem__('extra_args', extra_args)
    result_saving = libretaxi_saveUser.run(data_folder, **kwargs)

    if text == "/start":
        MenuID = "Menu_Init"
        extra_args.__setitem__("menu_txt", "Menu_Init")
        text = ""
        result_saving = libretaxi_saveUser.run(data_folder, **kwargs)
    elif text == "/cancel":
        MenuID = "Menu_Feed"
        extra_args.__setitem__("menu_txt", "Menu_Feed")
        text = ""
        result_saving = libretaxi_saveUser.run(data_folder, **kwargs)
    kwargs.__setitem__("prev_state", MenuID)
    kwargs.__setitem__("user", result_saving)
    if MenuID == "Menu_Init":
        return libretaxi_init_menu_handler.run(data_folder, **kwargs)
    elif MenuID == "Menu_AskLocation":
        return libretaxi_ask_location_menu_handler.run(data_folder, **kwargs)
    elif MenuID == "Menu_Feed":
        return libretaxi_feed_menu_handler.run(data_folder, **kwargs)
    elif MenuID == "Menu_Post":
        return libretaxi_post_menu_handler.run(data_folder, **kwargs)
    else:
        return result_saving
