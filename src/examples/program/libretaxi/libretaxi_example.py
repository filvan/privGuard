from src.examples.program.libretaxi.menu import libretaxi_handle_message


def run(data_folder, **kwargs):
    # translate that update is sent as input data when running privguard
    # translate only messages obtained from user that is not a chat
    pd = kwargs.get('pandas')
    return libretaxi_handle_message.run(data_folder, **kwargs)
