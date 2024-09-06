from src.examples.program.selfmailbot.celery import send_file
from src.examples.program.selfmailbot.helpers import get_subject


def run(data_folder, **kwargs):
    text = kwargs.get('extra_args').get('text')
    subject = get_subject(text)

    if text:
        subject = f"Photo: {get_subject(text)}"
    extra_args = kwargs.get('extra_args')
    extra_args.__setitem__('subject', subject)

    kwargs.__setitem__('extra_args', extra_args)

    return send_file.run(data_folder, **kwargs)
