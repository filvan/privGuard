def run(data_folder, **kwargs):
    pd = kwargs.get('pandas')
    ConsumerID = kwargs.get('extra_args').get('user_id')
    MenuID = kwargs.get('extra_args').get('menu_id')
    lon = kwargs.get('extra_args').get('lon')
    lat = kwargs.get('extra_args').get('lat')
    FirstName = kwargs.get('extra_args').get('first_name')
    LastName = kwargs.get('extra_args').get('last_name')
    LanguageCode = kwargs.get('extra_args').get('language_code')
    ReportCnt = kwargs.get('extra_args').get('report_cnt')
    ShadowBanned = kwargs.get('extra_args').get('shadow_banned')

    # saving of user based on previous research if user already exists
    libretaxi_users = pd.read_csv(data_folder + "users/data.csv")
    # check for userID duplicates
    if not libretaxi_users[libretaxi_users.ConsumerID == ConsumerID]:
        # get new id
        last_el = str(int(str(libretaxi_users.iloc[-1:].PostID)) + 1)

    # add to database the new user  with received infos

    return libretaxi_users.drop(
        ['ConsentUse', 'ConsentShare', 'ConsentSell', 'ConsentRetetention', 'ConsentCollection', 'ConsentRetention',
         'GuardianConsent', 'RequestDeletion', 'RequestDisclosure', 'RequestInaccurate'], axis=1)
