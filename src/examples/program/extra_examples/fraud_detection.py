
DTYPE = {
    'TransactionID': 'int32',
    'isFraud': 'int8',
    'TransactionDT': 'int32',
    'TransactionAmt': 'float32',
    'ProductCD': 'category',
    'card1': 'int16',
    'card2': 'float32',
    'card3': 'float32',
    'card4': 'category',
    'card5': 'float32',
    'card6': 'category',
    'addr1': 'float32',
    'addr2': 'float32',
    'dist1': 'float32',
    'dist2': 'float32',
    'P_emaildomain': 'category',
    'R_emaildomain': 'category',
}

IDX = 'TransactionID'
TGT = 'isFraud'

CCOLS = [f'C{i}' for i in range(1, 15)]
DCOLS = [f'D{i}' for i in range(1, 16)]
MCOLS = [f'M{i}' for i in range(1, 10)]
VCOLS = [f'V{i}' for i in range(1, 340)]

DTYPE.update((c, 'float32') for c in CCOLS)
DTYPE.update((c, 'float32') for c in DCOLS)
DTYPE.update((c, 'float32') for c in VCOLS)
DTYPE.update((c, 'category') for c in MCOLS)


DTYPE_ID = {
    'TransactionID': 'int32',
    'DeviceType': 'category',
    'DeviceInfo': 'category',
}

ID_COLS = [f'id_{i:02d}' for i in range(1, 39)]
ID_CATS = [
    'id_12', 'id_15', 'id_16', 'id_23', 'id_27', 'id_28', 'id_29', 'id_30',
    'id_31', 'id_33', 'id_34', 'id_35', 'id_36', 'id_37', 'id_38'
]

DTYPE_ID.update(((c, 'float32') for c in ID_COLS))
DTYPE_ID.update(((c, 'category') for c in ID_CATS))

IN_DIR = '../input'

NR = None
NTRAIN = 590540
params = {
    'num_leaves': 64,
    'objective': 'binary',
    'min_data_in_leaf': 10,
    'learning_rate': 0.1,
    'feature_fraction': 0.5,
    'bagging_fraction': 0.9,
    'bagging_freq': 1,
    'max_cat_to_onehot': 128,
    'metric': 'auc',
    'num_threads': 8,
    'seed': 42,
    'subsample_for_bin': uni.shape[0]
}
from os import path
from pandas.api.types import union_categoricals
def run(data_folder, **kwargs):
    np = kwargs.get('numpy')
    pd = kwargs.get('pandas')
    cross_validation = kwargs.get('cross_validation')
    metrics = kwargs.get('metrics')
    lgb = kwargs.get('lgb')
    model_selection = kwargs.get('model_selection')
    train_test_split = cross_validation.train_test_split
    roc_auc_score = metrics.roc_auc_score
    KFold = model_selection.KFold

    train = pd.read_csv(path.join(data_folder, 'train/data.csv'), schema=['TransactionID'])
    test = pd.read_csv(path.join(data_folder, 'test/data.csv'), schema=['TransactionID'])

    train['isTest'] = 0
    test['isTest'] = 1

    ntrain = train.shape[0]
    for c in train.columns:
        s = train[c]
        if hasattr(s, 'cat'):
            u = union_categoricals([train[c], test[c]], sort_categories=True)
            train[c] = u[:ntrain]
            test[c] = u[ntrain:]
    uni = train.append(test)
    uni['TimeInDay'] = uni.TransactionDT % 86400
    uni['Cents'] = uni.TransactionAmt % 1
    TGT = 'isTest'
    FEATS = uni.columns.tolist()
    FEATS.remove(TGT)
    FEATS.remove('TransactionDT')
    folds = list(KFold(n_splits=4, shuffle=True, random_state=42).split(uni[FEATS]))
    ds = lgb.Dataset(uni[FEATS], uni[TGT], params=params)
    s = LightGbmSnoop()
    res = lgb.cv(params,
                 ds,
                 folds=folds,
                 num_boost_round=3000,
                 early_stopping_rounds=100,
                 verbose_eval=100,
                 callbacks=[s._callback])