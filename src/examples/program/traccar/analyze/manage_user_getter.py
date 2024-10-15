def run(data_folder, **kwargs):
    pd = kwargs.get('pandas')
    columns = kwargs.get('extra_args').get('columns')[0]
    consumer_id = kwargs.get('extra_args').get('user_id')
    traccar_data = pd.read_csv(data_folder + "users/data.csv")
    traccar_data = traccar_data[traccar_data.ConsumerID == consumer_id]
    if columns == 'Password':
        return None
    return traccar_data[columns]
