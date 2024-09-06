from src.examples.program.selfmailbot.tpl import render_messages


def run(data_folder, **kwargs):
    render_messages("waiting_for_confirmation")
