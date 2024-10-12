#post_menu functions based on input user informations
from src.examples.program.libretaxi.repository import libretaxi_findUserAround, libretaxi_saveUser,libretaxi_savePost, \
    libretaxi_recentPosts
from src.examples.program.libretaxi.util.util import EscapeMarkdown
from src.examples.program.libretaxi import libretaxi_validation

def postToAdminChannel(text, user):
    #configure channel to send message I translated and set the message

    ParseMode = ""
    if len(user.Username) == 0 :
        #sets for message a parsingMode based on the username
        ParseMode = "MarkdownV2"
    #create a button for the user and the button will have this message: and it will cause to send a shadowban action message when clicking on it
    btnKeyboard = "☝️ Shadow ban"
    btnClick = "{\"Action\":\"SHADOW_BAN\",\"Id\":"+user.ConsumerID
    #message sent
    return user,text,ParseMode

def postToPublicChannel(text,user):
    # configure channel to send message I translated and set the message

    ParseMode = ""
    if len(user.Username) == 0:
        # sets for message a parsingMode based on the username
        ParseMode = "MarkdownV2"
    return user,text,ParseMode


def informUsersAround(data_folder, **kwargs):
    locales = kwargs.get('locales')
    pd = kwargs.get('pandas')
    libretaxi_posts = pd.read_csv(data_folder + "posts/data.csv")

    user = kwargs.get('extra_args').get('user')

    text = kwargs.get('extra_args').get('text')
    post_id = kwargs.get('extra_args').get('post_id')
    textWithContacts = ""

    if len(user.Username) == 0:
        userTextContact = "["+EscapeMarkdown(user.FirstName)+" "+EscapeMarkdown(user.LastName)+"](tg://user?id="+user.ConsumerID+")"
        textWithContacts = EscapeMarkdown(text)+"\n\n"+ locales.post_menu_via + " "+ userTextContact
    else:
        textWithContacts = EscapeMarkdown(text)+"\n\n"+ locales.post_menu_via + " "+ EscapeMarkdown(user.Username)

    if user.ShadowBanned != "Y":
        postToAdminChannel(textWithContacts,user)
        postToPublicChannel(textWithContacts,user)
    else:
        #send a message based on user shadow banned and post id so I return
        msg = textWithContacts + user.ConsumerID
        ParseMode =  ""
        if len(user.Username) == 0:
            # sets for message a parsingMode based on the username
            ParseMode = "MarkdownV2"
        return libretaxi_posts[libretaxi_posts.PostID == post_id]

    users_around = libretaxi_findUserAround.run(data_folder, **kwargs)

    for u in users_around:
        msg = textWithContacts + u.ConsumerID
        ParseMode =  ""
        if len(u.Username) == 0:
            # sets for message a parsingMode based on the username
            ParseMode = "MarkdownV2"
        btnKeyboard = locales.post_menu_report_button
        btnClick = "{\"Action\":\"REPORT_POST\",\"Id\":" + post_id
            # message sent
        return libretaxi_posts[libretaxi_posts.PostID == post_id]

def run(data_folder, **kwargs):
    locales = kwargs.get('locales')
    user_infos = kwargs.get('extra_args').get('user')
    text = kwargs.get('extra_args').get('text')
    if libretaxi_recentPosts.run(data_folder, **kwargs):
        msg = locales.post_menu_wait + user_infos['ConsumerID']
        #send previous message
        #update args
        extra_args = kwargs.get('extra_args')
        extra_args.__setitem__("menu_id","Menu_Feed")
        kwargs.__setitem__('extra_args',extra_args)
        return libretaxi_saveUser.run(data_folder, **kwargs)
    elif len(text) == 0:
        msg_driver = locales.post_menu_driver_example + user_infos['ConsumerID']
        msg_passanger = locales.post_menu_passenger_example + user_infos['ConsumerID']
        return user_infos
    else:

        errors = libretaxi_validation.run(text)
        if len(errors) > 0:
            msg = user_infos['Consumer_ID'] + errors + " "+locales.post_menu_or+"/cancel"
            return user_infos
        cleanText = text.strip()
        extra_args = kwargs.get('extra_args')
        extra_args.__setitem__("user_id",user_infos['ConsumerID'])
        extra_args.__setitem__("message_txt",cleanText)
        extra_args.__setitem__("lon", user_infos['Longitude'])
        extra_args.__setitem__("lat", user_infos['Latitude'])
        extra_args.__setitem__("reportCnt", 0)
        kwargs.__setitem__('extra_args',extra_args)

        results = libretaxi_savePost.run(data_folder, **kwargs)

        informUsersAround(user_infos['Longitude'], user_infos['Latitude'],cleanText, results, user_infos)

        msg = user_infos['ConsumerID']+locales.post_menu_sent

        extra_args = kwargs.get('extra_args')
        extra_args.__setitem__("menu_id","Menu_Feed")
        kwargs.__setitem__('extra_args',extra_args)
        return libretaxi_saveUser.run(data_folder, **kwargs)
