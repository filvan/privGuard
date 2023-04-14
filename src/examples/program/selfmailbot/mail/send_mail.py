def run(data_folder, **kwargs):
    to = kwargs.get('extra_args').get('to')
    subject = kwargs.get('extra_args').get('subject')
    text = kwargs.get('extra_args').get('text')

    # TODO set for privanal to None default
    attachment = kwargs.get('extra_args').get('attachment')
    # TODO set default ''
    attachment_name = kwargs.get('extra_args').get('attachment_name')

    pd = kwargs.get('pandas')
    selfmail_users = pd.read_csv(data_folder + "users/data.csv")
    selfmail_users = selfmail_users[selfmail_users.Email == to]

    message = to + subject + text
    if attachment is not None:
        message += (attachment + attachment_name)
    print(message)
    return selfmail_users