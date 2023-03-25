from src.examples.program.Libretaxi.repository import libretaxi_findUser,libretaxi_saveUser


def run(data_folder, **kwargs):
    print("Ask location menu")
    locales = kwargs.get('locales')
    user = kwargs.get('extra_args').get('user')

    if (user['Longitude'] != '') & (user['Latitude'] != ''):
        #save location
        message = "Saving location:"+ user['Longitude'] + " " + user['Latitude']
        print(message)
        extra_args = kwargs.get('extra_args')
        extra_args.__setitem__("menu_id","Menu_Feed")
        kwargs.__setitem__('extra_args',extra_args)
        return libretaxi_saveUser.run(data_folder, **kwargs)
    else:
        buttons = locales.ask_location_menu_next_button
        msg = user['ConsumerID'] + locales.ask_location_menu_click_next
        return libretaxi_findUser.run(data_folder, **kwargs)
