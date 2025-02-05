def run(data_folder, **kwargs):
    # Load the libraries.
    pd = kwargs.get('pandas')
    user_id = kwargs.get('extra_args').get('user_id')

    # Load the data / policies
    users = pd.read_csv(data_folder + "users/data.csv")

    # users = users[users.Age >= 18]
    users = users[users.ConsentProcessing == 'Y']

    """
    users = users[users.Gender == 'FEMALE']
    users = users.drop(axis=1, labels=['FirstName', 'LastName'])
    """
    # print("Mean age:", users.Age.mean())
    # print("\n")
    # print(users)

    users = users[users.NoLongerNecessary == 'Y']
    users = users[users.NecessaryForRightOfFreedomOfExpression == 'N']
    users = users[users.NecessaryForPublicInterestOrLegalObligation == 'N']
    users = users[users.NecessaryForLegalClaim == 'N']
    specific_user = users[users.DataSubjectID == user_id]
    specific_user = specific_user.drop(axis=1, labels=['FirstName', 'LastName', 'Age', 'Gender'])

    return specific_user
