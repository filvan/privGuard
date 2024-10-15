def run(data_folder,**kwargs):
    pd = kwargs.get('pandas')
    columns = kwargs.get('extra_args').get('columns')[0]
    new_val = kwargs.get('extra_args').get('new_val')
    data_subject_id = kwargs.get('extra_args').get('user_id')
    traccar_data = pd.read_csv(data_folder + "users/data.csv")
    traccar_data = traccar_data[traccar_data.DataSubjectID == data_subject_id]
    traccar_data[columns] = new_val
    return traccar_data
    # .drop(
    #    ['GuardianConsent', 'ConsentProcessingIdentifiable', 'RequestRectification', 'RequestDeletion',
    #     'RequestDisclosure', 'RequestProcessing', 'RequestDirectMarketing', 'ConsentTransfer'], axis=1))
