from celery import send_confirmation_mail


def run(data_folder, **kwargs):
    pd = kwargs.get('pandas')
    email = kwargs.get('extra_args').get('email')
    selfmail_users = pd.read_csv(data_folder + "users/data.csv")

    selfmail_users = selfmail_users[selfmail_users.Email == email]
    if selfmail_users:
        f = open('/templates/messages/email_is_occupied.txt', 'r')
        content = f.read()
        print(content)
        f.close()
    else:
        f = open('/templates/messages/confirmation_message_is_sent.txt', 'r')
        content = f.read()
        print(content)
        f.close()
        extra_args = kwargs.get('extra_args')
        extra_args.__setitem__('userid', selfmail_users.ConsumerID)

        kwargs.__setitem__('extra_args', extra_args)
        return send_confirmation_mail(data_folder,**kwargs)

    return selfmail_users
