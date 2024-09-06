from src.examples.program.selfmailbot.tpl import render_messages


def run(data_folder, **kwargs):
    pd = kwargs.get('pandas')
    user_id = kwargs.get('extra_args').get('user_id')
    key = kwargs.get('extra_args').get('key')

    selfmailbot_users = pd.read_csv(data_folder + "data.csv")

    specific_user = selfmailbot_users[selfmailbot_users.ConsumerID == user_id]

    if specific_user.ConfirmationLink != key:
        render_messages("confirmation_failure")
    else:
        specific_user.IsConfirmed = 'Y'
        render_messages("email_is_confirmed")
    return specific_user.drop(
        ['ConsentUse', 'ConsentShare', 'ConsentShare', 'ConsentSell', 'ConsentCollection', 'GuardianConsent',
         'RequestDeletion', 'RequestDisclosure', 'RequestInaccurate', 'LimitUse', 'Age'], axis=1)
