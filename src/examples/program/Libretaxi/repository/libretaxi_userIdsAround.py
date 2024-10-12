def run(data_folder, **kwargs):
    pd = kwargs.get('pandas')
    lon = kwargs.get('extra_args').get('lon')
    lat = kwargs.get('extra_args').get('lat')

    libretaxi_users = pd.read_csv(data_folder + "users/data.csv")
    libretaxi_users = libretaxi_users[libretaxi_users.Longitude == lon]
    libretaxi_users = libretaxi_users[libretaxi_users.Latitude == lat]

    return libretaxi_users['DataSubjectID']
