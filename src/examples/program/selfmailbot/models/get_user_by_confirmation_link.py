def run(data_folder, **kwargs):
    pd = kwargs.get('pandas')
    link = kwargs.get('extra_args').get('link')

    selfmail_users = pd.read_csv(data_folder + "data.csv")
    selfmail_users = selfmail_users[selfmail_users.ConfirmationLink == link]

    return selfmail_users.drop(
        ['ConsentUse', 'ConsentShare', 'ConsentShare', 'ConsentSell', 'ConsentCollection', 'GuardianConsent',
         'RequestDeletion', 'RequestDisclosure', 'RequestInaccurate', 'LimitUse', 'Age'], axis=1)