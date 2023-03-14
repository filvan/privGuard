from src.examples.program.Libretaxi.repository import libretaxi_saveUser
from src.examples.program.Libretaxi.locales.english import *

def saveLocation(data_folder, **kwargs):
   return 8

def run(data_folder, **kwargs):
    pd = kwargs.get('pandas')
    print("Ask location menu")
    user = kwargs.get('extra_args').get('user')

    if user.Longitude & user.Latitude:
        #save location
        message = "Saving location:"+ user.Longitude + " " + user.Latitude
        print(message)
        extra_args = kwargs.get('extra_args')
        extra_args.__setitem__("menu_id","Menu_Feed")
        kwargs.__setitem__('extra_args',extra_args)
        return libretaxi_saveUser.run(data_folder, **kwargs)
    else:
        buttons = ask_location_menu_next_button
        msg = user.ConsumerID + ask_location_menu_click_next

        return user
