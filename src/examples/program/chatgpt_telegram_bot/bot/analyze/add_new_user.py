def run(data_folder, **kwargs):
    pd = kwargs.get('pandas')
    DataSubjectID = kwargs.get('extra_args').get('user_id')
    chat_id = kwargs.get('extra_args').get('chat_id')
    username = kwargs.get('extra_args').get('username')
    first_name = kwargs.get('extra_args').get('first_name')
    last_name = kwargs.get('extra_args').get('last_name')
    raise_exception = kwargs.get('extra_args').get('raise_exception')

    users = pd.read_csv(data_folder + "users/data.csv")
    specific_user = users[users.DataSubjectID == DataSubjectID]

    if not specific_user and raise_exception:
        raise ValueError(f"User {DataSubjectID} does not exist")

    return users
