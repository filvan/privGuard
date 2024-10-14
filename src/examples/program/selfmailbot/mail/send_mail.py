def run(data_folder, **kwargs):
    to = kwargs.get('extra_args').get('email')
    subject = kwargs.get('extra_args').get('subject')
    text = kwargs.get('extra_args').get('text')
    attachment = kwargs.get('extra_args').get('attachment')
    attachment_name = kwargs.get('extra_args').get('attachment_name')
    pd = kwargs.get('pandas')

    selfmailbot_users = pd.read_csv(data_folder + "data.csv")
    specific_user = selfmailbot_users[selfmailbot_users.Email == to]

    message = to + subject + text
    if attachment is not None:
        message += (attachment + attachment_name)
    print(message)

    return specific_user
