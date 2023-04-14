from ..mail import send_mail

def run(data_folder, **kwargs):
    user_id = kwargs.get('extra_args').get('user_id')
    pd = kwargs.get('pandas')
    selfmail_users = pd.read_csv(data_folder + "users/data.csv")
    selfmail_users = selfmail_users[selfmail_users.ConsumerID == user_id]

    extra_args = kwargs.get('extra_args')
    extra_args.__setitem__('to', selfmail_users.Email)

    kwargs.__setitem__('extra_args', extra_args)
    send_mail.run(data_folder, **kwargs)

    return selfmail_users.drop(
        ['ConsentUse', 'ConsentShare', 'ConsentShare', 'ConsentSell', 'ConsentCollection', 'GuardianConsent',
         'RequestDeletion', 'RequestDisclosure', 'RequestInaccurate', 'LimitUse', 'Age'], axis=1)