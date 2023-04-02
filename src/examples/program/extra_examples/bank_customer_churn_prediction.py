from os import path

def run(data_folder, **kwargs):

    pd = kwargs.get('pandas')

    # Read the training dataset
    training_data = pd.read_csv(path.join(data_folder, 'data.csv'))
    # Drop the irrelevant columns  as shown above
    training_data = training_data.drop(["RowNumber", "ConsumerID", "Surname"], axis=1)


    target_col = ["Exited"]

    # Print the first 5 lines of the dataset
    # View the dimension of the dataset
    training_data.shape

    percentage_labels = training_data.groupby(by='Exited')
    return percentage_labels
