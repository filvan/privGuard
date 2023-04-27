import os
file_dir = os.path.dirname(os.path.realpath('__file__'))
def run(data_folder, **kwargs):
    file_name = os.path.join(file_dir, 'examples/program/selfmailbot/templates/messages/hello_message.txt')
    file_name = os.path.abspath(os.path.realpath(file_name))
    f = open(file_name, 'r')
    content = f.read()
    print(content)
    f.close()
