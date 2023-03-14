set(List).intersection(set(All_feature_new_extra))

import numpy as np
import pandas as pd
import datetime
import gc
import matplotlib.pyplot as plt
import seaborn as sns
import lightgbm as lgb
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import mean_squared_error
from scipy.stats import ks_2samp
from tqdm import tqdm
import os

def run(data_folder, **kwargs):
    print(os.listdir("../input"))
    df_train_old = pd.read_pickle("../input/features-from-old-model/train_old_features.pkl")
    df_test_old = pd.read_pickle("../input/features-from-old-model/test_old_features.pkl")
    df_train = pd.read_pickle("../input/elo-features-data-7-feb/train_df.pkl")
    df_test = pd.read_pickle("../input/elo-features-data-7-feb/test_df.pkl")
    int_train = set(df_train_old.columns).intersection(df_train.columns) - set(['card_id'])
    int_test = set(df_test_old.columns).intersection(df_test.columns)- set(['card_id'])
    df_train.drop(columns = int_train, inplace = True)
    df_test.drop(columns = int_test, inplace = True)
    df_train = pd.merge(df_train, df_train_old, on = 'card_id')
    df_test = pd.merge(df_test,df_test_old, on = 'card_id')
    del df_train_old, df_test_old
    df_train_columns = list(df_test.columns) #+ ['outliers']

    df_train_columns = set(df_train_columns)-set(["card_id", "old_purchase_date_max", "old_purchase_date_min",
     "new_purchase_date_max", "new_purchase_date_min", "first_active_month"])

    df_train_columns= list(df_train_columns)

    df_train_columns= List[0:250] + All_feature_new_extra[0:350]
    # #[c for c in df_train.columns if c not in ['card_id', 'first_active_month','target','outliers']]

    # ##All_featrures[0:105]#
    #=============================== Comparing distributions ===========================================

    list_p_value =[]

    for i in tqdm(df_train_columns):
        list_p_value.append(ks_2samp(df_test[i] , df_train[i])[1])

    Se = pd.Series(list_p_value, index = df_train_columns).sort_values()
    list_discarded = list(Se[Se < .2].index)

    # #==============================
    df_train_columns = features_current_model[0:200]
    df_train_columns = list(set(df_train_columns) - set(list_discarded))
    len(df_train_columns)
    target = df_train['target']
    del df_train['target'] #, df_train['target_x']
    import gc
    gc.collect()
    df_oof = pd.DataFrame()
    df_oof['card_id']= df_train['card_id']
    df_oof['target'] = target
    param = {'num_leaves': 62,
             'min_data_in_leaf': 20,
             'objective': 'regression',
             'max_depth': 8,
             'learning_rate': 0.001,
             "min_child_samples": 20,
             "boosting": "gbdt",
             "feature_fraction": 0.9,
             "bagging_freq": 1,
             "bagging_fraction": 0.9,
             "bagging_seed": 11,
             "metric": 'rmse',
             "lambda_l1": 0.1,
             "verbosity": -1,
             "nthread": 4,
             "random_state": 4590}
    # ,
    # "max_bin": 3000


    for i in range(1):
        folds = StratifiedKFold(n_splits=10, shuffle=True, random_state=4590)
        oof = np.zeros(len(df_train))
        predictions = np.zeros(len(df_test))
        feature_importance_df = pd.DataFrame()

    list_regressor = []
    # list_rmse = []

    for fold_, (trn_idx, val_idx) in enumerate(folds.split(df_train, df_train['outliers'].values)):
        print("fold {}".format(fold_))
        trn_data = lgb.Dataset(df_train.iloc[trn_idx][df_train_columns],
                               label=target.iloc[trn_idx])  # , categorical_feature=categorical_feats)
        val_data = lgb.Dataset(df_train.iloc[val_idx][df_train_columns],
                               label=target.iloc[val_idx])  # , categorical_feature=categorical_feats)

        num_round = 50000
        clf = lgb.train(param, trn_data, num_round, valid_sets=[trn_data, val_data], verbose_eval=500,
                        early_stopping_rounds=500)
        oof[val_idx] = clf.predict(df_train.iloc[val_idx][df_train_columns], num_iteration=clf.best_iteration)

        fold_importance_df = pd.DataFrame()
        fold_importance_df["Feature"] = df_train_columns
        fold_importance_df["importance"] = clf.feature_importance()
        fold_importance_df["fold"] = fold_ + 1
        feature_importance_df = pd.concat([feature_importance_df, fold_importance_df], axis=0)

        predictions += clf.predict(df_test[df_train_columns], num_iteration=clf.best_iteration) / folds.n_splits

        list_regressor.append(clf)

    print(np.sqrt(mean_squared_error(oof, target)))

    df_oof['oof'] = oof
    df_oof.to_csv("oof.csv")
    cols = (feature_importance_df[["Feature", "importance"]]
            .groupby("Feature")
            .mean()
            .sort_values(by="importance", ascending=False)[:1000].index)

    best_features = feature_importance_df.loc[feature_importance_df.Feature.isin(cols)]

    plt.figure(figsize=(20,40))
    sns.barplot(x="importance",
                y="Feature",
                data=best_features.sort_values(by="importance",
                                               ascending=False))
    plt.title('LightGBM Features (avg over folds)')
    plt.tight_layout()
    plt.show()
    plt.savefig('lgbm_importances.png')
    fip = best_features.sort_values(by="importance",ascending=False)
    plt.figure(figsize=(20,40))
    imp = fip.groupby('Feature')['importance'].mean().sort_values(ascending=True)
    imp.to_csv("feature_importance.csv")
    imp.plot('barh')
    plt.show()
    Se_imp = fip.groupby('Feature')['importance'].mean().sort_values(ascending=False)
    print(list(Se_imp.index))
    for i in range(1):
        sub_df = pd.DataFrame({"card_id":df_test["card_id"].values})
        sub_df["target"] = predictions
        sub_df.to_csv("submission.csv", index=False)