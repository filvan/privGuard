from src.examples.program.selfmailbot.mail import send_mail
from src.examples.program.selfmailbot.tpl import render_email


def run(data_folder, **kwargs):
    text = render_email('confirmation')

    extra_args = kwargs.get('extra_args')
    extra_args.__setitem__('to', extra_args.get('to'))
    extra_args.__setitem__('subject', '[Selfmailbot] Please confirm your email')
    extra_args.__setitem__('text', text)
    kwargs.__setitem__('extra_args', extra_args)

    return send_mail.run(data_folder, **kwargs)
