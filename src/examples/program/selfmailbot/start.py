
def run(data_folder, **kwargs):
    f = open('/templates/messages/hello_message.txt', 'r')
    content = f.read()
    print(content)
    f.close()
