def run(data_folder, **kwargs):
    # Load the libraries.
    pd = kwargs.get('pandas')

    # Load the data / policies
    gdpr = pd.read_csv(data_folder + "data.csv")

    # Filter
    gdpr = gdpr[gdpr.ConsentProcessing == 'Y']
    gdpr = gdpr[gdpr.Age >= 16]
    # gdpr = gdpr.PersonalData

    return gdpr
