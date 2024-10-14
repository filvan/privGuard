import os


def get_template(template_name: str):
    project_dir = os.path.dirname(os.path.realpath('__file__'))
    file_dir = os.path.join(project_dir, "examples/program/selfmailbot")
    return os.path.join(file_dir, template_name)


def render_messages(tpl: str):
    template = get_template("templates/messages/" + tpl + ".txt")
    file_name = os.path.abspath(os.path.realpath(template))
    f = open(file_name, 'r')
    content = f.read()
    print(content)
    f.close()


def render_email(tpl: str):
    template = get_template("templates/email/" + tpl + ".txt")
    file_name = os.path.abspath(os.path.realpath(template))
    f = open(file_name, 'r')
    content = f.read()
    f.close()
    return content


def render_html(tpl: str):
    template = get_template("templates/html/" + tpl + ".txt")
    file_name = os.path.abspath(os.path.realpath(template))
    f = open(file_name, 'r')
    content = f.read()
    print(content)
    f.close()
