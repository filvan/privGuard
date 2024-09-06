from src.examples.program.selfmailbot.celery import send_confirmation_mail
from src.examples.program.selfmailbot.tpl import render_messages


def run(data_folder, **kwargs):
    pd = kwargs.get('pandas')
    email = kwargs.get('extra_args').get('email')
    selfmailbot_users = pd.read_csv(data_folder + "data.csv")

    specific_user = selfmailbot_users[selfmailbot_users.Email == email]
    if specific_user:
        render_messages("email_is_occupied")
    else:
        render_messages("message_is_sent")
        extra_args = kwargs.get('extra_args')
        extra_args.__setitem__('userid', selfmailbot_users.ConsumerID)

        kwargs.__setitem__('extra_args', extra_args)
        send_confirmation_mail.run(data_folder, **kwargs)

    return selfmailbot_users
