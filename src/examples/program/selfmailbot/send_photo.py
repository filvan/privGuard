from celery import send_file
from .helpers import get_subject
def run(data_folder, **kwargs):
    text = kwargs.get('extra_args').get('text')
    subject = get_subject(text)
    f = open('/templates/messages/message_is_sent.txt', 'r')
    content = f.read()
    print(content)
    f.close()
    if text:
        subject = 'Photo: {}'.format(get_subject(text))
    extra_args = kwargs.get('extra_args')
    extra_args.__setitem__('subject', subject)

    kwargs.__setitem__('extra_args', extra_args)
    f = open('/templates/messages/photo_is_sent.txt', 'r')
    content = f.read()
    print(content)
    f.close()
    return send_file.run(data_folder, **kwargs)