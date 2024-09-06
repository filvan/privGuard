from src.examples.program.selfmailbot.models import get_user_by_confirmation_link
from src.examples.program.selfmailbot.tpl import render_html


def run(data_folder, **kwargs):
    user = get_user_by_confirmation_link.run(data_folder, **kwargs)
    if user is None:
        render_html('confirmation_failure')
    else:
        render_html('confirmation_ok')
        user.isConfirmed = 'Y'
    return user
