from src.examples.program.selfmailbot.celery import send_text
from src.examples.program.selfmailbot.helpers import get_subject
from src.examples.program.selfmailbot.tpl import render_messages


def run(data_folder, **kwargs):
    text = kwargs.get('extra_args').get('text')
    subject = get_subject(text)
    render_messages("message_is_sent")
    extra_args = kwargs.get('extra_args')
    extra_args.__setitem__('subject', subject)

    kwargs.__setitem__('extra_args', extra_args)

    return send_text.run(data_folder, **kwargs)
