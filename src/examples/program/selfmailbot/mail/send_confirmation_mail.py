import send_mail
def run(data_folder, **kwargs):
    f = open('/templates/messages/confirmation.txt', 'r')
    content = f.read()

    f.close()
    extra_args = kwargs.get('extra_args')
    extra_args.__setitem__('to', extra_args.get('email'))
    extra_args.__setitem__('subject', '[Selfmailbot] Please confirm your email')
    extra_args.__setitem__('text',content)
    kwargs.__setitem__('extra_args', extra_args)

    return send_mail.run(data_folder, **kwargs)