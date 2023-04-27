from src.examples.program.selfmailbot.celery import send_confirmation_mail


import os
file_dir = os.path.dirname(os.path.realpath('__file__'))
def run(data_folder, **kwargs):
    pd = kwargs.get('pandas')
    email = kwargs.get('extra_args').get('email')
    selfmail_users = pd.read_csv(data_folder + "data.csv")

    selfmail_users = selfmail_users[selfmail_users.Email == email]
    if selfmail_users:
        file_name = os.path.join(file_dir, 'examples/program/selfmailbot/templates/messages/email_is_occupied.txt')
        file_name = os.path.abspath(os.path.realpath(file_name))
        f = open(file_name, 'r')
        content = f.read()
        print(content)
        f.close()
    else:
        file_name = os.path.join(file_dir, 'examples/program/selfmailbot/templates/messages/confirmation_message_is_sent.txt')
        file_name = os.path.abspath(os.path.realpath(file_name))
        f = open(file_name, 'r')
        content = f.read()
        print(content)
        f.close()
        extra_args = kwargs.get('extra_args')
        extra_args.__setitem__('userid', selfmail_users.ConsumerID)

        kwargs.__setitem__('extra_args', extra_args)
        return send_confirmation_mail(data_folder,**kwargs)

    return selfmail_users
