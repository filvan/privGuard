def run(data_folder, **kwargs):
    # Load the libraries.
    pd = kwargs.get('pandas')

    # Load the data / policies
    patients = pd.read_csv(data_folder + "patients/data.csv")

    # print(patients)
    # print('Policy: ' + str(patients.policy))

    patients = patients[patients.GENDER == 'FEMALE']
    # print(patients)
    patients = patients[patients.AGE >= 18]
    # print(patients)
    patients = patients['ID']
    # print(patients)

    # print(patients.policy.notes)
    return patients
