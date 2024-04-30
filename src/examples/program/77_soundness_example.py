def run(data_folder, **kwargs):
    # Load the libraries.
    pd = kwargs.get('pandas')

    # Load the data / policies
    patients = pd.read_csv(data_folder + "patients/data.csv", ['ID', 'NAME', 'AGE', 'GENDER'])

    print(patients)
    print('Policy: ' + str(patients.policy))

    # patients = patients[patients.NAME == 'John']
    patients = patients[patients.AGE >= 18]
    # patients = patients[patients.GENDER == 'FEMALE']

    # print(patients)
    return patients
