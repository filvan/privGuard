from src.examples.program.selfmailbot.celery import send_text
from src.examples.program.selfmailbot.helpers import get_subject
import os
file_dir = os.path.dirname(os.path.realpath('__file__'))
def run(data_folder, **kwargs):
    text = kwargs.get('extra_args').get('text')
    subject = get_subject(text)
    file_name = os.path.join(file_dir, 'examples/program/selfmailbot/templates/messages/message_is_sent.txt')
    file_name = os.path.abspath(os.path.realpath(file_name))
    f = open(file_name, 'r')
    content = f.read()
    print(content)
    f.close()
    extra_args = kwargs.get('extra_args')
    extra_args.__setitem__('subject', subject)

    kwargs.__setitem__('extra_args', extra_args)

    return send_text.run(data_folder, **kwargs)