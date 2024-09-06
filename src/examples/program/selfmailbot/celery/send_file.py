from src.examples.program.selfmailbot.mail import send_mail


def run(data_folder, **kwargs):
    user_id = kwargs.get('extra_args').get('user_id')
    pd = kwargs.get('pandas')
    selfmailbot_users = pd.read_csv(data_folder + "data.csv")
    specific_user = selfmailbot_users[selfmailbot_users.ConsumerID == user_id]

    extra_args = kwargs.get('extra_args')
    extra_args.__setitem__('to', specific_user.Email)

    kwargs.__setitem__('extra_args', extra_args)
    send_mail.run(data_folder, **kwargs)

    return specific_user.drop(
        ['ConsentUse', 'ConsentShare', 'ConsentShare', 'ConsentSell', 'ConsentCollection', 'GuardianConsent',
         'RequestDeletion', 'RequestDisclosure', 'RequestInaccurate', 'LimitUse', 'Age'], axis=1)
