import os

file_dir = os.path.dirname(os.path.realpath('__file__'))


def run(data_folder, **kwargs):
    pd = kwargs.get('pandas')
    user_id = kwargs.get('extra_args').get('user_id')
    key = kwargs.get('extra_args').get('key')

    selfmailbot_users = pd.read_csv(data_folder + "data.csv")

    specific_user = selfmailbot_users[selfmailbot_users.ConsumerID == user_id]

    if specific_user.ConfirmationLink != key:
        file_name = os.path.join(file_dir, 'examples/program/selfmailbot/templates/messages/confirmation_failure.txt')
        file_name = os.path.abspath(os.path.realpath(file_name))
        f = open(file_name, 'r')
        content = f.read()
        print(content)
        f.close()
    else:
        specific_user.IsConfirmed = 'Y'
        file_name = os.path.join(file_dir, 'examples/program/selfmailbot/templates/messages/email_is_confirmed.txt')
        file_name = os.path.abspath(os.path.realpath(file_name))
        f = open(file_name, 'r')
        content = f.read()
        print(content)
        f.close()
    return selfmailbot_users.drop(
        ['ConsentUse', 'ConsentShare', 'ConsentShare', 'ConsentSell', 'ConsentCollection', 'GuardianConsent',
         'RequestDeletion', 'RequestDisclosure', 'RequestInaccurate', 'LimitUse', 'Age'], axis=1)
