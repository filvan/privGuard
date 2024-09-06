from src.examples.program.selfmailbot.mail import send_mail
import os

file_dir = os.path.dirname(os.path.realpath('__file__'))


def run(data_folder, **kwargs):
    file_name = os.path.join(file_dir, 'examples/program/selfmailbot/templates/email/confirmation.txt')
    file_name = os.path.abspath(os.path.realpath(file_name))
    f = open(file_name, 'r')
    content = f.read()
    f.close()

    extra_args = kwargs.get('extra_args')
    extra_args.__setitem__('to', extra_args.get('email'))
    extra_args.__setitem__('subject', '[Selfmailbot] Please confirm your email')
    extra_args.__setitem__('text', content)
    kwargs.__setitem__('extra_args', extra_args)

    return send_mail.run(data_folder, **kwargs)
