from celery import send_confirmation_mail

def run(data_folder, **kwargs):
    pd = kwargs.get('pandas')
    user_id = kwargs.get('extra_args').get('user_id')
    selfmail_users = pd.read_csv(data_folder + "users/data.csv")

    selfmail_users = selfmail_users[selfmail_users.ConsumerID == user_id]

    f = open('/templates/messages/confirmation_message_is_sent.txt', 'r')
    content = f.read()
    print(content + selfmail_users.Email)
    f.close()
    return send_confirmation_mail.run(data_folder, **kwargs)