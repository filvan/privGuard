def run(data_folder, **kwargs):
    pd = kwargs.get('pandas')
    DataSubjectID = kwargs.get('extra_args').get('user_id')
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
    if not libretaxi_users[libretaxi_users.DataSubjectID == DataSubjectID]:
        # get new id
        last_el = str(int(str(libretaxi_users.iloc[-1:].DataSubjectID)) + 1)

    # add to database the new user  with received infos

    return libretaxi_users.drop(
        ['ConsentProcessing', 'GuardianConsentProcessing', 'Age', 'DataSubjectCanLiftProhibition',
         'ConsentProcessingIdentifiable', 'ManifestlyMadePublicByDataSubject', 'RequireRectification',
         'NoLongerNecessary', 'NecessaryForRightOfFreedomOfExpression', 'NecessaryForPublicInterestOrLegalObligation',
         'NecessaryForLegalClaim', 'Objection&NoOverridingLegitimateGrounds', 'ObjectionToProcessingForDirectMarketing',
         'UnlawfullyProcessed', 'ToBeErasedForComplianceWithLegalObligation',
         'InRelationToOfferOfInformationSocietyServices', 'RequestPortability', 'ObjectionToSpecificKindOfProcessing',
         'CompellingLegitimateGrounds', 'ConsentDirectMarketing', 'ConsentTransfer', 'InfoFromRegister', 'ConsentData',
         'SpecialPersonalData', 'CriminalData', 'InfoAboutController&DPO&Processing&Recipients',
         'StoragePeriod&DataSubjectRightsAndObligations', 'StoragePeriod&DataSubjectRights&Source',
         'InfoAboutProcessing&Recipients&StoragePeriod&DataSubjectRights&Source', 'ConsentDirectMarketingData',
         'PersonalDataUnderAppropriateSafeguards&Conditions', 'Date', 'MenuID'], axis=1)
