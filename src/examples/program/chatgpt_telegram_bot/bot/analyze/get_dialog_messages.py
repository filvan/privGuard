def run(data_folder, **kwargs):
    pd = kwargs.get('pandas')
    DataSubjectID = kwargs.get('extra_args').get('user_id')
    raise_exception = kwargs.get('extra_args').get('raise_exception')
    DialogID = kwargs.get('extra_args').get('dialog_id')

    users = pd.read_csv(data_folder + "users/data.csv")
    specific_user = users[users.DataSubjectID == DataSubjectID]

    if not specific_user and raise_exception:
        raise ValueError(f"User {DataSubjectID} does not exist")

    dialogs = pd.read_csv(data_folder + "dialogs/data.csv")
    specific_dialog = dialogs[dialogs.DialogID == DialogID]

    return specific_dialog
