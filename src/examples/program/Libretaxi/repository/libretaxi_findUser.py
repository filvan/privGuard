def run(data_folder, **kwargs):
    pd = kwargs.get('pandas')
    user_id = kwargs.get('extra_args').get('user_id')

    libretaxi_users = pd.read_csv(data_folder + "users/data.csv")

    libretaxi_users = libretaxi_users[libretaxi_users.DataSubjectID == user_id]

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
