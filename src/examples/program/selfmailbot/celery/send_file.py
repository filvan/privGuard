from src.examples.program.selfmailbot.mail import send_mail


def run(data_folder, **kwargs):
    user_id = kwargs.get('extra_args').get('user_id')
    subject = kwargs.get('extra_args').get('subject')
    text = kwargs.get('extra_args').get('text')
    attachment = kwargs.get('extra_args').get('attachment')
    attachment_name = kwargs.get('extra_args').get('attachment_name')
    pd = kwargs.get('pandas')

    selfmailbot_users = pd.read_csv(data_folder + "data.csv")
    specific_user = selfmailbot_users[selfmailbot_users.ConsumerID == user_id]

    extra_args = kwargs.get('extra_args')
    extra_args.__setitem__('to', specific_user.Email)
    extra_args.__setitem__('text', text)
    extra_args.__setitem__('subject', subject)
    extra_args.__setitem__('attachment', attachment)
    extra_args.__setitem__('attachment_name', attachment_name)

    kwargs.__setitem__('extra_args', extra_args)
    send_mail.run(data_folder, **kwargs)

    return specific_user.drop(
        ['ConsentUse', 'ConsentShare', 'ConsentShare', 'ConsentSell', 'ConsentCollection', 'GuardianConsent',
         'RequestDeletion', 'RequestDisclosure', 'RequestInaccurate', 'LimitUse', 'Age'], axis=1)
