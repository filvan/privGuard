from src.examples.program.traccar.analyze import manage_user_getter
def run(data_folder, **kwargs):
    pd = kwargs.get('pandas')
    extra_args = kwargs.get('extra_args')
    extra_args.__setitem__('columns', ['Mail'])

    return manage_user_getter.run(data_folder,**kwargs)