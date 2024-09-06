import os
from src.examples.program.selfmailbot.models import get_user_by_confirmation_link

file_dir = os.path.dirname(os.path.realpath('__file__'))


def run(data_folder, **kwargs):
    user = get_user_by_confirmation_link.run(data_folder, **kwargs)
    if user is None:
        file_name = os.path.join(file_dir, 'examples/program/selfmailbot/templates/html/confirmation_failure.html')
    else:
        file_name = os.path.join(file_dir, 'examples/program/selfmailbot/templates/html/ok.html')
        user.isConfirmed = 'Y'
    file_name = os.path.abspath(os.path.realpath(file_name))
    f = open(file_name, 'r')
    content = f.read()
    print(content)
    f.close()
    return user
