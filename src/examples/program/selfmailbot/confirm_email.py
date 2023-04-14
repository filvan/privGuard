def run(data_folder, **kwargs):
    pd = kwargs.get('pandas')
    user_id = kwargs.get('extra_args').get('user_id')
    key = kwargs.get('extra_args').get('key')
    selfmail_users = pd.read_csv(data_folder + "users/data.csv")

    selfmail_users = selfmail_users[selfmail_users.ConsumerID == user_id]

    if(selfmail_users.ConfirmationLink != key):
        f = open('/templates/messages/confirmation_failure.txt', 'r')
        content = f.read()
        print(content)
        f.close()
    else:
        selfmail_users.IsConfirmed = 'Y'
        f = open('/templates/messages/email_is_confirmed.txt', 'r')
        content = f.read()
        print(content)
        f.close()
    return selfmail_users.drop(
        ['ConsentUse', 'ConsentShare', 'ConsentShare', 'ConsentSell', 'ConsentCollection', 'GuardianConsent',
         'RequestDeletion', 'RequestDisclosure', 'RequestInaccurate', 'LimitUse', 'Age'], axis=1)