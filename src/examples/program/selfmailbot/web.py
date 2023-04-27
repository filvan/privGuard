from src.examples.program.selfmailbot.models import get_user_by_confirmation_link
def run(data_folder, **kwargs):
    user = get_user_by_confirmation_link.run(data_folder,**kwargs)
    if user is not None:
        user.isConfirmed = 'Y'

    return user