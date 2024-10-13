def run(data_folder, **kwargs):
    pd = kwargs.get('pandas')
    post_id = kwargs.get('extra_args').get('post_id')

    libretaxi_posts = pd.read_csv(data_folder + "posts/data.csv")
    libretaxi_posts = libretaxi_posts[libretaxi_posts.PostID == post_id]

    return libretaxi_posts.drop(
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
