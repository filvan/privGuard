from src.examples.program.selfmailbot.tpl import render_messages


def run(data_folder, **kwargs):
    pd = kwargs.get('pandas')
    user_id = kwargs.get('extra_args').get('user_id')

    selfmailbot_users = pd.read_csv(data_folder + "data.csv")

    specific_user = selfmailbot_users[selfmailbot_users.DataSubjectID == user_id]
    # specific_user = specific_user[specific_user.CorrectInfos == 'N']
    # specific_user.CorrectInfos = 'Y'
    specific_user.IsConfirmed = 'N'

    specific_user.Email = ''
    render_messages("email_is_reset")
    return specific_user
