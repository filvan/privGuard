from src.examples.program.selfmailbot.celery import send_confirmation_mail
import os

file_dir = os.path.dirname(os.path.realpath('__file__'))


def run(data_folder, **kwargs):
    pd = kwargs.get('pandas')
    user_id = kwargs.get('extra_args').get('user_id')
    selfmailbot_users = pd.read_csv(data_folder + "data.csv")

    specific_user = selfmailbot_users[selfmailbot_users.ConsumerID == user_id]
    file_name = os.path.join(file_dir,
                             'examples/program/selfmailbot/templates/messages/confirmation_message_is_sent.txt')
    file_name = os.path.abspath(os.path.realpath(file_name))
    f = open(file_name, 'r')
    content = f.read()
    print(content)
    f.close()
    return send_confirmation_mail.run(data_folder, **kwargs)
