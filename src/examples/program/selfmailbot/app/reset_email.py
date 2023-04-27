import os
file_dir = os.path.dirname(os.path.realpath('__file__'))
def run(data_folder, **kwargs):
    pd = kwargs.get('pandas')
    user_id = kwargs.get('extra_args').get('user_id')

    selfmail_users = pd.read_csv(data_folder + "data.csv")

    selfmail_users = selfmail_users[selfmail_users.ConsumerID == user_id]
    selfmail_users = selfmail_users[selfmail_users.CorrectInfos == 'N']
    #selfmail_users.CorrectInfos = 'Y'
    selfmail_users.IsConfirmed = 'N'


    selfmail_users.Email = ''
    file_name = os.path.join(file_dir, 'examples/program/selfmailbot/templates/messages/email_is_reset.txt')
    file_name = os.path.abspath(os.path.realpath(file_name))
    f = open(file_name, 'r')
    content = f.read()
    print(content)
    f.close()
    return selfmail_users