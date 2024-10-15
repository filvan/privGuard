def run(data_folder, **kwargs):
    pd = kwargs.get('pandas')
    columns = kwargs.get('extra_args').get('columns')[0]
    data_subject_id = kwargs.get('extra_args').get('user_id')
    traccar_data = pd.read_csv(data_folder + "users/data.csv")
    traccar_data = traccar_data[traccar_data.DataSubjectID == data_subject_id]
    if columns == 'Password':
        return None
    return traccar_data[columns]
