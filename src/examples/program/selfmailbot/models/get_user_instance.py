def run(data_folder, **kwargs):
    pd = kwargs.get('pandas')
    user_id = kwargs.get('extra_args').get('user_id')

    selfmailbot_users = pd.read_csv(data_folder + "data.csv")
    specific_user = selfmailbot_users[selfmailbot_users.DataSubjectID == user_id]

    return specific_user.drop(
        ['ConsentUse', 'ConsentShare', 'ConsentShare', 'ConsentSell', 'ConsentCollection', 'GuardianConsent',
         'RequestDeletion', 'RequestDisclosure', 'RequestInaccurate', 'LimitUse', 'Age'], axis=1)
