from src.examples.program.libretaxi.repository import libretaxi_findUser, libretaxi_saveUser


def run(data_folder, **kwargs):
    print("Feed menu")
    locales = kwargs.get('locales')
    text = kwargs.get('extra_args').get('text')
    user = kwargs.get('extra_args').get('user')
    if len(text) == 0 and user['Longitude'] == '' and user['Latitude'] == '':
        msg = user['DataSubjectID'] + locales.feed_menu_greeting
    elif text == locales.feed_menu_search_button:
        extra_args = kwargs.get('extra_args')
        extra_args.__setitem__("menu_id", "Menu_Post")
        kwargs.__setitem__('extra_args', extra_args)
        return libretaxi_saveUser.run(data_folder, **kwargs)
    elif user['Longitude'] != '' and user['Latitude'] != '':
        extra_args = kwargs.get('extra_args')
        extra_args.__setitem__("lon", user['Longitude'])
        extra_args.__setitem__("lat", user['Latitude'])
        kwargs.__setitem__('extra_args', extra_args)
        return libretaxi_saveUser.run(data_folder, **kwargs)
