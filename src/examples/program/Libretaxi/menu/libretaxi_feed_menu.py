from src.examples.program.Libretaxi.repository import libretaxi_findUser,libretaxi_saveUser


def run(data_folder, **kwargs):
    print("Feed menu")
    locales = kwargs.get('locales')
    text = kwargs.get('extra_args').get('text')
    user = kwargs.get('extra_args').get('user')
    if len(text) == 0 and not ((user['Longitude'] != '') & (user['Latitude'] != '')):
        msg = user['ConsumerID'] + locales.feed_menu_greeting
        return libretaxi_findUser.run(data_folder, **kwargs)
    elif text == locales.feed_menu_search_button:
        extra_args = kwargs.get('extra_args')
        extra_args.__setitem__("menu_id","Menu_Post")
        kwargs.__setitem__('extra_args',extra_args)
        return libretaxi_saveUser.run(data_folder, **kwargs)
    else:
        msg = user['ConsumerID'] + locales.feed_menu_error
        return libretaxi_findUser.run(data_folder, **kwargs)