from src.examples.program.selfmailbot.mail import send_mail
from src.examples.program.selfmailbot.tpl import render_email


def run(data_folder, **kwargs):
    user_id = kwargs.get('extra_args').get('user_id')
    pd = kwargs.get('pandas')

    selfmailbot_users = pd.read_csv(data_folder + "data.csv")
    specific_user = selfmailbot_users[selfmailbot_users.DataSubjectID == user_id]

    extra_args = kwargs.get('extra_args')
    extra_args.__setitem__('to', specific_user.Email)
    extra_args.__setitem__('subject', '[Selfmailbot] Confirm your email')
    text = render_email('confirmation')

    extra_args.__setitem__('text', text + str(specific_user.ConfirmationLink[0]))
    kwargs.__setitem__('extra_args', extra_args)

    return send_mail.run(data_folder, **kwargs)
