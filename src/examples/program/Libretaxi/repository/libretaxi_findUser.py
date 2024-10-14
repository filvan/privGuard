def run(data_folder, **kwargs):
    pd = kwargs.get('pandas')
    user_id = kwargs.get('extra_args').get('user_id')

    libretaxi_users = pd.read_csv(data_folder + "users/data.csv")

    libretaxi_users = libretaxi_users[libretaxi_users.DataSubjectID == user_id]

    return libretaxi_users
