

def run(data_folder, **kwargs):
    pd = kwargs.get('pandas')

    #saving of user based on previous research if user already exists
    libretaxi_users = pd.read_csv(data_folder + "users/data.csv")
    libretaxi_posts = pd.read_csv(data_folder + "posts/data.csv")
    #two separated database, one for folder and one for user
    #need to look for the user in the database if it already exists
    libretaxi_users = libretaxi_users[libretaxi_users.ConsumerID == 'n_consumer']
    new_user_infos = libretaxi_posts.iloc[-1:]
    libretaxi_users['Username'] = new_user_infos.Username
    libretaxi_users['FirstName'] = new_user_infos.FirstName
    libretaxi_users['LastName'] = new_user_infos.LastName
    libretaxi_users['LanguageCode'] = new_user_infos.LanguageCode
    return libretaxi_users.iloc[-1:0].drop(['ConsentUse', 'ConsentShare', 'ConsentSell', 'ConsentRetetention', 'ConsentCollection', 'ConsentRetention','GuardianConsent', 'RequestDeletion', 'RequestDisclosure', 'RequestInaccurate'], axis=1)