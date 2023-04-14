from celery import send_text
from .helpers import get_subject

def run(data_folder, **kwargs):
    text = kwargs.get('extra_args').get('text')
    subject = get_subject(text)
    f = open('/templates/messages/message_is_sent.txt', 'r')
    content = f.read()
    print(content)
    f.close()
    extra_args = kwargs.get('extra_args')
    extra_args.__setitem__('subject', subject)

    kwargs.__setitem__('extra_args', extra_args)

    return send_text.run(data_folder, **kwargs)