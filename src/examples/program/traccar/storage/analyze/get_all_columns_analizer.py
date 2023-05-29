def run(data_folder, **kwargs):

    pd = kwargs.get('pandas')
    clazz = kwargs.get('extra_args').get('clazz')

    if str(clazz) == 'Device':
        traccar_data = pd.read_csv(data_folder + "devices/data.csv")
    elif str(clazz) == 'User':
        traccar_data = pd.read_csv(data_folder + "users/data.csv")
    elif str(clazz) == 'Position':
        traccar_data = pd.read_csv(data_folder + "positions/data.csv")

    return traccar_data.iloc[-1:0].drop(
        ['ConsentUse', 'ConsentShare', 'ConsentSell', 'ConsentRetetention', 'ConsentCollection', 'ConsentRetention',
         'GuardianConsent', 'RequestDeletion', 'RequestDisclosure', 'RequestInaccurate'], axis=1)
