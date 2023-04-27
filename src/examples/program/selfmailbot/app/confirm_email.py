import os
file_dir = os.path.dirname(os.path.realpath('__file__'))
def run(data_folder, **kwargs):
    pd = kwargs.get('pandas')
    user_id = kwargs.get('extra_args').get('user_id')
    key = kwargs.get('extra_args').get('key')

    selfmail_users = pd.read_csv(data_folder + "data.csv")

    selfmail_users = selfmail_users[selfmail_users.ConsumerID == user_id]

    if selfmail_users.ConfirmationLink != key:
        file_name = os.path.join(file_dir, 'examples/program/selfmailbot/templates/messages/confirmation_failure.txt')
        file_name = os.path.abspath(os.path.realpath(file_name))
        f = open(file_name, 'r')
        content = f.read()
        print(content)
        f.close()
    else:
        selfmail_users.IsConfirmed = 'Y'
        file_name = os.path.join(file_dir, 'examples/program/selfmailbot/templates/messages/email_is_confirmed.txt')
        file_name = os.path.abspath(os.path.realpath(file_name))
        f = open(file_name, 'r')
        content = f.read()
        print(content)
        f.close()
    return selfmail_users.drop(
        ['ConsentUse', 'ConsentShare', 'ConsentShare', 'ConsentSell', 'ConsentCollection', 'GuardianConsent',
         'RequestDeletion', 'RequestDisclosure', 'RequestInaccurate', 'LimitUse', 'Age'], axis=1)