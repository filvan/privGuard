from ..mail import send_mail
def run(data_folder, **kwargs):
    user_id = kwargs.get('extra_args').get('user_id')
    pd = kwargs.get('pandas')
    selfmail_users = pd.read_csv(data_folder + "users/data.csv")
    selfmail_users = selfmail_users[selfmail_users.ConsumerID == user_id]
    f = open('/templates/email/confirmation.txt', 'r')
    content = f.read()
    extra_args = kwargs.get('extra_args')
    extra_args.__setitem__('to',selfmail_users.Email)
    extra_args.__setitem__('subject','[Selfmailbot] Confirm your email')

    extra_args.__setitem__('text',content+selfmail_users.ConfirmationLink)
    kwargs.__setitem__('extra_args', extra_args)
    send_mail.run(data_folder,**kwargs)

    return selfmail_users.drop(
        ['ConsentUse', 'ConsentShare', 'ConsentShare', 'ConsentSell', 'ConsentCollection', 'GuardianConsent',
         'RequestDeletion', 'RequestDisclosure', 'RequestInaccurate', 'LimitUse', 'Age'], axis=1)