#TODO: no ACTUAL CLASSIFIER IN THE EXAMPLE WHY?
from os import path
def run(data_folder, **kwargs):
    pd = kwargs.get('pandas')
    np = kwargs.get('numpy')
    xgb = kwargs.get('xgboost')
    train_df = pd.read_csv(path.join(data_folder, 'data.csv'))
    train_df.shape
    train_df.head()

    ulimit = np.percentile(train_df.logerror.values, 99)
    llimit = np.percentile(train_df.logerror.values, 1)
    train_df['logerror'].ix[train_df['logerror']>ulimit] = ulimit
    train_df['logerror'].ix[train_df['logerror']<llimit] = llimit

    train_df['transaction_month'] = train_df['transactiondate'].dt.month

    cnt_srs = train_df['transaction_month'].value_counts()
    plt.figure(figsize=(12,6))
    sns.barplot(cnt_srs.index, cnt_srs.values, alpha=0.8, color=color[3])
    plt.xticks(rotation='vertical')
    plt.xlabel('Month of transaction', fontsize=12)
    plt.ylabel('Number of Occurrences', fontsize=12)
    plt.show()
    (train_df['parcelid'].value_counts().reset_index())['parcelid'].value_counts()
    prop_df = pd.read_csv("../input/properties_2016.csv")
    prop_df.shape
    prop_df.head()
    missing_df = prop_df.isnull().sum(axis=0).reset_index()
    missing_df.columns = ['column_name', 'missing_count']
    missing_df = missing_df.ix[missing_df['missing_count']>0]
    missing_df = missing_df.sort_values(by='missing_count')

    ind = np.arange(missing_df.shape[0])
    width = 0.9
    fig, ax = plt.subplots(figsize=(12,18))
    rects = ax.barh(ind, missing_df.missing_count.values, color='blue')
    ax.set_yticks(ind)
    ax.set_yticklabels(missing_df.column_name.values, rotation='horizontal')
    ax.set_xlabel("Count of missing values")
    ax.set_title("Number of missing values in each column")
    plt.show()
    plt.figure(figsize=(12,12))
    sns.jointplot(x=prop_df.latitude.values, y=prop_df.longitude.values, size=10)
    plt.ylabel('Longitude', fontsize=12)
    plt.xlabel('Latitude', fontsize=12)
    plt.show()
    train_df = pd.merge(train_df, prop_df, on='parcelid', how='left')
    train_df.head()
    pd.options.display.max_rows = 65

    dtype_df = train_df.dtypes.reset_index()
    dtype_df.columns = ["Count", "Column Type"]
    dtype_df
    dtype_df.groupby("Column Type").aggregate('count').reset_index()
    missing_df = train_df.isnull().sum(axis=0).reset_index()
    missing_df.columns = ['column_name', 'missing_count']
    missing_df['missing_ratio'] = missing_df['missing_count'] / train_df.shape[0]
    missing_df.ix[missing_df['missing_ratio']>0.999]
    mean_values = train_df.mean(axis=0)
    train_df_new = train_df.fillna(mean_values, inplace=True)

    # Now let us look at the correlation coefficient of each of these variables #
    x_cols = [col for col in train_df_new.columns if col not in ['logerror'] if train_df_new[col].dtype == 'float64']

    labels = []
    values = []
    for col in x_cols:
        labels.append(col)
        values.append(np.corrcoef(train_df_new[col].values, train_df_new.logerror.values)[0, 1])
    corr_df = pd.DataFrame({'col_labels': labels, 'corr_values': values})
    corr_df = corr_df.sort_values(by='corr_values')

    ind = np.arange(len(labels))
    width = 0.9
    fig, ax = plt.subplots(figsize=(12, 40))
    rects = ax.barh(ind, np.array(corr_df.corr_values.values), color='y')
    ax.set_yticks(ind)
    ax.set_yticklabels(corr_df.col_labels.values, rotation='horizontal')
    ax.set_xlabel("Correlation coefficient")
    ax.set_title("Correlation coefficient of the variables")
    # autolabel(rects)
    plt.show()
    corr_zero_cols = ['assessmentyear', 'storytypeid', 'pooltypeid2', 'pooltypeid7', 'pooltypeid10', 'poolcnt', 'decktypeid', 'buildingclasstypeid']
    for col in corr_zero_cols:
        print(col, len(train_df_new[col].unique()))
    corr_df_sel = corr_df.ix[(corr_df['corr_values']>0.02) | (corr_df['corr_values'] < -0.01)]
    corr_df_sel
    cols_to_use = corr_df_sel.col_labels.tolist()

    temp_df = train_df[cols_to_use]
    corrmat = temp_df.corr(method='spearman')
    f, ax = plt.subplots(figsize=(8, 8))

    # Draw the heatmap using seaborn
    sns.heatmap(corrmat, vmax=1., square=True)
    plt.title("Important variables correlation map", fontsize=15)
    plt.show()
    col = "finishedsquarefeet12"
    ulimit = np.percentile(train_df[col].values, 99.5)
    llimit = np.percentile(train_df[col].values, 0.5)
    train_df[col].ix[train_df[col]>ulimit] = ulimit
    train_df[col].ix[train_df[col]<llimit] = llimit

    plt.figure(figsize=(12,12))
    sns.jointplot(x=train_df.finishedsquarefeet12.values, y=train_df.logerror.values, size=10, color=color[4])
    plt.ylabel('Log Error', fontsize=12)
    plt.xlabel('Finished Square Feet 12', fontsize=12)
    plt.title("Finished square feet 12 Vs Log error", fontsize=15)
    plt.show()
    col = "calculatedfinishedsquarefeet"
    ulimit = np.percentile(train_df[col].values, 99.5)
    llimit = np.percentile(train_df[col].values, 0.5)
    train_df[col].ix[train_df[col]>ulimit] = ulimit
    train_df[col].ix[train_df[col]<llimit] = llimit

    col = "taxamount"
    ulimit = np.percentile(train_df[col].values, 99.5)
    llimit = np.percentile(train_df[col].values, 0.5)
    train_df[col].ix[train_df[col]>ulimit] = ulimit
    train_df[col].ix[train_df[col]<llimit] = llimit

    train_y = train_df['logerror'].values
    cat_cols = ["hashottuborspa", "propertycountylandusecode", "propertyzoningdesc", "fireplaceflag", "taxdelinquencyflag"]
    train_df = train_df.drop(['parcelid', 'logerror', 'transactiondate', 'transaction_month']+cat_cols, axis=1)


    xgb_params = {
        'eta': 0.05,
        'max_depth': 8,
        'subsample': 0.7,
        'colsample_bytree': 0.7,
        'objective': 'reg:linear',
        'silent': 1,
        'seed' : 0
    }
    dtrain = xgb.DMatrix(train_df, train_y, feature_names=train_df.columns.values)
    model = xgb.train(dict(xgb_params, silent=0), dtrain, num_boost_round=50)

    # plot the important features #
    xgb.plot_importance(model, max_num_features=50, height=0.8, ax=ax)





