

def run(data_folder, **kwargs):

    # Load the libraries.
    pd = kwargs.get('pandas')

    # Load the data / policies
    cpra = pd.read_csv(data_folder + "data.csv")


    # Filter
    cpra = cpra[cpra.ConsentShare == 'Y']
    cpra = cpra[cpra.Age >= 16]
    #cpra = cpra.PersonalInformation


    return cpra.PersonalInformation