def run(data_folder, **kwargs):
    pd = kwargs.get('pandas')
    clazz = kwargs.get('extra_args').get('clazz')
    columns = kwargs.get('extra_args').get('columns')
    conditions = kwargs.get('extra_args').get('conditions')
    sort_cond = kwargs.get('extra_args').get('sort_cond')
    traccar_data = []
    if str(clazz) == 'Device':
        traccar_data = pd.read_csv(data_folder + "devices/data.csv")
    elif str(clazz) == 'User':
        traccar_data = pd.read_csv(data_folder + "users/data.csv")
    elif str(clazz) == 'Position':
        traccar_data = pd.read_csv(data_folder + "positions/data.csv")
    traccar_data = traccar_data[columns]
    if conditions is not None:
        for cond in conditions:
            traccar_data = traccar_data[cond]
    if sort_cond is not None:
        traccar_data = traccar_data.sort_values(by=sort_cond[0], axis=1, ascending=sort_cond[1])
    return traccar_data
