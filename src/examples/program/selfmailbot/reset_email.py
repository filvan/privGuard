def run(data_folder, **kwargs):
    pd = kwargs.get('pandas')
    user_id = kwargs.get('extra_args').get('user_id')

    selfmail_users = pd.read_csv(data_folder + "users/data.csv")

    selfmail_users = selfmail_users[selfmail_users.ConsumerID == user_id]
    selfmail_users.RequestInaccurate = 'N'
    selfmail_users.IsConfirmed = 'N'
    selfmail_users = selfmail_users[selfmail_users.RequestInaccurate == 'N']

    f = open('/templates/messages/email_is_reset.txt', 'r')
    content = f.read()
    print(content)
    f.close()
    return selfmail_users.drop(
        ['ConsentUse', 'ConsentShare', 'ConsentShare', 'ConsentSell', 'ConsentCollection', 'GuardianConsent',
         'RequestDeletion', 'RequestDisclosure', 'RequestInaccurate', 'LimitUse', 'Age'], axis=1)