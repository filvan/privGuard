from src.examples.program.Libretaxi.menu import libretaxi_menu


def run(data_folder, **kwargs):
    #translate that update is sent as input data when running privguard
    #translate only messages obtained from user that is not a chat
    pd = kwargs.get('pandas')
    return libretaxi_menu.run(data_folder, **kwargs)
