def run(data_folder, **kwargs):

    pd = kwargs.get('pandas')
    clazz = kwargs.get('extra_args').get('clazz')

    if str(clazz) == 'Device':
        traccar_data = pd.read_csv(data_folder + "devices/data.csv")
    elif str(clazz) == 'User':
        traccar_data = pd.read_csv(data_folder + "users/data.csv")
    elif str(clazz) == 'Position':
        traccar_data = pd.read_csv(data_folder + "positions/data.csv")
    else:
        return "No valid input clazz"

    return traccar_data
        #.drop(
        #['GuardianConsent','ConsentProcessingIdentifiable','RequestRectification','RequestDeletion','RequestDisclosure','RequestProcessing','RequestDirectMarketing','ConsentTransfer'], axis=1)

