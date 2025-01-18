from datetime import datetime


def run(data_folder, **kwargs):
    pd = kwargs.get('pandas')
    DataSubjectID = kwargs.get('extra_args').get('user_id')
    raise_exception = kwargs.get('extra_args').get('raise_exception')
    Dialog_id = kwargs.get('extra_args').get('dialog_id')
    chat_mode = kwargs.get('extra_args').get('chat_mode')
    start_time = datetime.now()
    model = kwargs.get('extra_args').get('model')
    messages = kwargs.get('extra_args').get('messages')

    users = pd.read_csv(data_folder + "users/data.csv")
    specific_user = users[users.DataSubjectID == DataSubjectID]

    if not specific_user and raise_exception:
        raise ValueError(f"User {DataSubjectID} does not exist")

    return Dialog_id
