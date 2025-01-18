def run(data_folder, **kwargs):
    pd = kwargs.get('pandas')
    DataSubjectID = kwargs.get('extra_args').get('user_id')
    raise_exception = kwargs.get('extra_args').get('raise_exception')

    users = pd.read_csv(data_folder + "users/data.csv")
    specific_user = users[users.DataSubjectID == DataSubjectID]

    if specific_user:
        return True
    else:
        if raise_exception:
            raise ValueError(f"User {DataSubjectID} does not exist")
        else:
            return False
