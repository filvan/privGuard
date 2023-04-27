from src.examples.program.selfmailbot.mail import send_mail
import os
file_dir = os.path.dirname(os.path.realpath('__file__'))
def run(data_folder, **kwargs):
    user_id = kwargs.get('extra_args').get('user_id')
    pd = kwargs.get('pandas')
    selfmail_users = pd.read_csv(data_folder + "data.csv")
    selfmail_users = selfmail_users[selfmail_users.ConsumerID == user_id]

    file_name = os.path.join(file_dir, 'examples/program/selfmailbot/templates/email/confirmation.txt')
    file_name = os.path.abspath(os.path.realpath(file_name))
    f = open(file_name, 'r')
    content = f.read()
    extra_args = kwargs.get('extra_args')
    #extra_args.__setitem__('to',selfmail_users.Email)
    extra_args.__setitem__('subject','[Selfmailbot] Confirm your email')

    extra_args.__setitem__('text',content+str(selfmail_users.ConfirmationLink[0]))
    kwargs.__setitem__('extra_args', extra_args)
    send_mail.run(data_folder,**kwargs)

    return selfmail_users.drop(
        ['ConsentUse', 'ConsentShare', 'ConsentShare', 'ConsentSell', 'ConsentCollection', 'GuardianConsent',
         'RequestDeletion', 'RequestDisclosure', 'RequestInaccurate', 'LimitUse', 'Age'], axis=1)