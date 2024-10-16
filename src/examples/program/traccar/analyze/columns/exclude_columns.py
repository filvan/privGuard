def run(data_folder, **kwargs):

    pd = kwargs.get('pandas')
    clazz = kwargs.get('extra_args').get('clazz')
    columns = kwargs.get('extra_args').get('columns')

    if str(clazz) == 'Device':
        traccar_data = pd.read_csv(data_folder + "devices/data.csv")
    elif str(clazz) == 'User':
        traccar_data = pd.read_csv(data_folder + "users/data.csv")
    elif str(clazz) == 'Position':
        traccar_data = pd.read_csv(data_folder + "positions/data.csv")
    else:
        return "Wrong input clazz"

    return traccar_data.drop(columns, axis=1)
    # drop(['ConsentUse', 'ConsentShare', 'ConsentSell', 'ConsentRetetention', 'ConsentCollection', 'ConsentRetention','GuardianConsent', 'RequestDeletion', 'RequestDisclosure', 'RequestInaccurate'], axis=1)
