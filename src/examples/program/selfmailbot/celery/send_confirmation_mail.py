from src.examples.program.selfmailbot.mail import send_mail
import os

file_dir = os.path.dirname(os.path.realpath('__file__'))


def run(data_folder, **kwargs):
    user_id = kwargs.get('extra_args').get('user_id')
    pd = kwargs.get('pandas')
    selfmailbot_users = pd.read_csv(data_folder + "data.csv")
    specific_user = selfmailbot_users[selfmailbot_users.ConsumerID == user_id]

    file_name = os.path.join(file_dir, 'examples/program/selfmailbot/templates/email/confirmation.txt')
    file_name = os.path.abspath(os.path.realpath(file_name))
    f = open(file_name, 'r')
    content = f.read()
    extra_args = kwargs.get('extra_args')
    # extra_args.__setitem__('to',specific_user.Email)
    extra_args.__setitem__('subject', '[Selfmailbot] Confirm your email')

    extra_args.__setitem__('text', content + str(specific_user.ConfirmationLink[0]))
    kwargs.__setitem__('extra_args', extra_args)
    send_mail.run(data_folder, **kwargs)

    return specific_user.drop(
        ['ConsentUse', 'ConsentShare', 'ConsentShare', 'ConsentSell', 'ConsentCollection', 'GuardianConsent',
         'RequestDeletion', 'RequestDisclosure', 'RequestInaccurate', 'LimitUse', 'Age'], axis=1)
