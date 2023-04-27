from src.examples.program.selfmailbot.celery import send_file
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
    if text:
        subject = 'Photo: {}'.format(get_subject(text))
    extra_args = kwargs.get('extra_args')
    extra_args.__setitem__('subject', subject)

    kwargs.__setitem__('extra_args', extra_args)
    file_name = os.path.join(file_dir, 'examples/program/selfmailbot/templates/messages/photo_is_sent.txt')
    file_name = os.path.abspath(os.path.realpath(file_name))
    f = open(file_name, 'r')

    content = f.read()
    print(content)
    f.close()
    return send_file.run(data_folder, **kwargs)