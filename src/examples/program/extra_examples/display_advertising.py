import warnings
warnings.filterwarnings('ignore')

import gc, itertools, time, math
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import category_encoders as ce
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix, log_loss, roc_auc_score
from sklearn.preprocessing import OneHotEncoder, KBinsDiscretizer, LabelEncoder, RobustScaler
from catboost import CatBoostClassifier
from xgboost import XGBClassifier
from lightgbm import plot_metric
from sklearn.model_selection import train_test_split

def robust_transfer(df):
    '''transfer multiple columns using robustscaler
       对连续型字段使用robustscaler
    '''
    start = time.time()
    Scaler = RobustScaler().fit(df)
    df1 = Scaler.transform(df)
    print("encoding is over! the program costs {:.2f} seconds".format(time.time() - start))
    return df1

#train0 = robust_transfer(train[features])
#test0 = robust_transfer(test[features])

def cut_bins(df, con_cols, qnumbers):
    '''cut columns into bins
       对连续型字段进行分桶
    '''
    start = time.time()
    for col in con_cols:
        df[col] = pd.qcut(df[col], qnumbers, duplicates='drop')
        print('processing: {}'.format(col))
    print("cutting is over! the program costs {:.2f} seconds".format(time.time() - start))
    return df
def transfrom_target_encoder(dt_all, cat_features):
    start = time.time()
    for col in cat_features:
        dt_all[col] = ce.TargetEncoder().fit_transform(dt_all[col], dt_all['Label'])
    print("encoding is over! the program costs {:.2f} seconds".format(time.time() - start))
    return dt_all


def transfrom_target_encoder0(train, test, cat_features):
    '''fit on train data, transfrom test data
    '''
    start = time.time()
    ce_target_encoder = ce.TargetEncoder(cols = cat_features).fit(train, train['Label'])
    train = ce_target_encoder.transform(train)
    test['Label'] = np.nan
    test = ce_target_encoder.transform(test)
    print("encoding is over! the program costs {:.2f} seconds".format(time.time() - start))
    return train, test

def transfrom_count_encoder(dt_all, cat_features):
    start = time.time()
    for col in cat_features:
        dt_all[col] = ce.CountEncoder().fit_transform(dt_all[col])
    print("encoding is over! the program costs {:.2f} seconds".format(time.time() - start))
    return dt_all

def transfrom_label_encoder(dt_all, cat_features):
    '''do label encoding
    '''
    start = time.time()
    for col in cat_features:
        dt_all[col] = LabelEncoder().fit_transform(dt_all[col]).astype(str)
        print('processing: {}'.format(col))
    print("encoding is over! the program costs {:.2f} seconds".format(time.time() - start))
    return dt_all

def cross_features(df, features, outputFeaturelist = False):
    '''generate synthetic features
    '''
    start = time.time()
    for col in features:
        for col2 in features:
            feature_name = col + 'X' + col2
            features.append(feature_name)
            df[feature_name] = df[col] * df[col2]
        print('processing: {}'.format(col))
    print("encoding is over! the program costs {:.2f} seconds".format(time.time() - start))
    if outputFeaturelist:
        return df, features
    else:
        return df


def plot_catboost(y_label):
    '''plot catboost learning curve
    '''
    learn_error = pd.read_csv('./catboost_info/learn_error.tsv', sep='\t')
    test_error = pd.read_csv('./catboost_info/test_error.tsv', sep='\t')
    metric = pd.concat([learn_error, test_error.iloc[:, 1]], axis=1)
    metric.columns = ['iterations', 'train', 'test']
    plt.rcParams['figure.facecolor'] = 'white'
    metric.plot(x='iterations', y=['train', 'test'])
    plt.ylabel(y_label)
    plt.grid()
    plt.show()


def plot_confusion_matrix(cm, classes, normalize=False, title='Confusion matrix', cmap=plt.cm.Blues):
    '''This function prints and plots the confusion matrix.
       Normalization can be applied by setting `normalize=True`.
    '''
    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        print("Normalized confusion matrix")
    else:
        print('Confusion matrix, without normalization')

    print(cm)
    plt.rcParams['figure.facecolor'] = 'white'
    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes)
    plt.yticks(tick_marks, classes)

    fmt = '.2f' if normalize else 'd'
    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, format(cm[i, j], fmt),
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")

    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')


def feature_selection(features, feature_importance, DISTRI=0.7, selection=False, plot=True):
    '''do feature selection
    '''
    feimp = pd.DataFrame({'feature': features,
                          'importance': feature_importance}).sort_values(by=['importance'],
                                                                         ascending=False)
    if selection:
        feimp = feimp.iloc[: int(feimp.shape[0] * DISTRI), ]
    else:
        pass

    if plot:
        plt.figure(figsize=(7, 10))
        sns.barplot(data=feimp, x='importance', y='feature')
        plt.title('Catboost Feature Importances')
    else:
        pass
    return feimp


def run(data_folder, **kwargs):
    continue_var = ['I' + str(i) for i in range(1, 14)]
    cat_features = ['C' + str(i) for i in range(1,27)]
    col_names_train = ['Label'] + continue_var + cat_features
    col_names_test = col_names_train[1:]

    reader = pd.read_csv('/kaggle/input/criteo-dataset/dac/train.txt', sep='\t',
                         names=col_names_train, chunksize=100000, iterator=True)

    train = pd.DataFrame()
    start = time.time()
    for i, chunk in enumerate(reader):
        if train.shape[0] > 1000000:
            break
        train = pd.concat([train, chunk.sample(frac=.05, replace=False, random_state=911)], axis=0)
        # print(train.shape[0])
        if i % 20 == 0:
            print('Processing Chunk No. {}'.format(i))
    print('Reading data costs %.2f seconds'%(time.time() - start))

    #train = pd.read_csv('/kaggle/input/criteo-dataset/dac/train.txt',
    #                       sep='\t', names=col_names_train,
    #                       chunksize=100000) # ten chunks: first 1,000,000

    test = pd.read_csv('/kaggle/input/criteo-dataset/dac/test.txt',sep='\t', names=col_names_test)
    #train = train.get_chunk(1000000)
    print('train has {} rows and {} columns'.format(train.shape[0], train.shape[1]))
    print('test has {} rows and {} columns'.format(test.shape[0], test.shape[1]))
    train.info()
    ls = list(train.columns)
    ls.remove('Label')

    unbalance = []
    short = []
    print('输出原始数据枚举值对照表')
    print('-'*50)
    for i in ls:
        train_len = len(train[i].astype(str).value_counts())
        test_len = len(test[i].astype(str).value_counts())
        if (test_len > train_len) and test_len > 100 and train[i].dtype == 'object':
            unbalance.append(i)
        elif (test_len > train_len) and test_len <= 100 and train[i].dtype == 'object':
            short.append(i)
        else:
            pass
        print(i, ' | train: {} | test：{}'.format(train_len, test_len))
    print('合并长尾枚举值，使分类特征在训练集与测试集分布一致')
    print('-'*50)
    DISTRI = 0.7 # 数字越大，则枚举值分得越多越详细
    start = time.time()
    for col in short:
        print('processing: {}'.format(col))
        d1 = train[col].astype(str).value_counts()  # 训练集频数表
        envalue = d1[: int(len(d1) * DISTRI)].index   # 取按照频数排序后前n%项目的枚举值
        train[col] = np.where(train[col].isin(envalue), train[col], 'longtail')
        test[col] = np.where(test[col].isin(envalue) , test[col], 'longtail')
    print("the program costs {:.2f} seconds".format(time.time() - start))

    DISTRI = 0.5 # 数字越大，则枚举值分得越多越详细
    start = time.time()
    for col in unbalance:
        print('processing: {}'.format(col))
        d1 = train[col].astype(str).value_counts()  # 训练集频数表
        envalue = d1[: int(len(d1) * DISTRI)].index   # 取按照频数排序后前n%项目的枚举值
        train[col] = np.where((train[col].isin(envalue)) | (train[col].isna()) , train[col], 'longtail')
        test[col] = np.where((test[col].isin(envalue)) | (test[col].isna()), test[col], 'longtail')
    print("the program costs {:.2f} seconds".format(time.time() - start))
    print('\n')
    print('输出经过处理后的枚举值对照表')
    print('-'*50)
    for i in ls:
        train_len = len(train[i].astype(str).value_counts())
        test_len = len(test[i].astype(str).value_counts())
        print(i, ' | train: {} | test：{}'.format(train_len, test_len))
    train.info()
    fill_mean = lambda x: x.fillna(x.mean())
    start = time.time()
    for col in continue_var:
        print('filling NA value of {} ...'.format(i))
        train[col] = train[col].groupby(train['C7']).apply(fill_mean)
        test[col] = test[col].groupby(test['C7']).apply(fill_mean)
        train[col] = train[col].fillna(test[col].mean())
        test[col] = test[col].fillna(test[col].mean())
        train[col] = train[col].astype('float64')
        test[col] = test[col].astype('float64')
    print("filling NA costs {:.2f} seconds".format(time.time() - start))

    train = train.fillna('unknown')
    test = test.fillna('unknown')
    TRAIN_LEN = len(train)
    test.info()
    train['I13_I6'] = train['I13'] * train['I6']
    test['I13_I6'] = test['I13'] * test['I6']
    y_train = train[['Label']]
    x_train = train.drop(['Label'], axis=1)
    x_train, x_val, y_train, y_val = train_test_split(x_train, y_train, test_size=0.20, stratify=y_train, random_state=256)
    x_train
    model = CatBoostClassifier(
        iterations=100,
        learning_rate=0.4,
        task_type='GPU',
        loss_function='Logloss',
        depth=8,
    )

    fit_model = model.fit(
        x_train, y_train,
        eval_set=(x_val, y_val),
        cat_features = cat_features,
        verbose=10
    )

    feature_im = fit_model.feature_importances_
    feimp = feature_selection(x_train.columns, feature_im, 0.7)
    feimp
    feimp = feature_selection(x_train.columns, feature_im, 0.7, selection=True, plot=False)
    feimp
    x_train = x_train[feimp['feature']]
    x_val = x_val[feimp['feature']]
    test = test[feimp['feature']]
    cat_features0 = [i for i in feimp['feature'] if 'C' in i]
    model = CatBoostClassifier(
        iterations=100,
        learning_rate=0.4,
        task_type='GPU',
        loss_function='Logloss',
         #gpu_ram_part=0.9,
         #boosting_type='Plain',
         #max_ctr_complexity=2,
         depth=8,
         #gpu_cat_features_storage='CpuPinnedMemory'
    )

    fit_model = model.fit(
        x_train, y_train,
        eval_set=(x_val, y_val),
        cat_features=cat_features0,
        verbose=10
    )

    feature_im = fit_model.feature_importances_

    plot_catboost('logloss')


    y_test = model.predict(test,
                           prediction_type='Probability',
                           ntree_end=model.get_best_iteration(),
                           thread_count=-1,
                           verbose=None)

    y_val_pred = model.predict(x_val,
                           prediction_type='Probability',
                           ntree_start=0,
                           ntree_end=model.get_best_iteration(),
                           thread_count=-1,
                           verbose=None)

    y_test_pred = y_test[:,1]
    y_val_pred = y_val_pred[:,1]
    y_val_class = np.where(y_val_pred > 0.5,1,0)
    print('Out of folds logloss is {:.4f}'.format(log_loss(y_val, y_val_pred)))

    submission = pd.read_csv('../input/criteo-display-ad-challenge/random_submission.zip', compression='zip')
    submission = pd.DataFrame({'Id': submission['Id'], 'Predicted': y_test_pred })
    submission.to_csv('submission.csv',index = False)

    submission = pd.DataFrame({'Id': submission['Id'], 'Predicted': y_test_pred * 0.98})
    submission.to_csv('submission2.csv',index = False)

    submission = pd.DataFrame({'Id': submission['Id'], 'Predicted': y_test_pred * 1.02})
    submission.to_csv('submission3.csv',index = False)
    submission
    feimp = pd.DataFrame({'feature': x_train.columns,
                  'importance': feature_im }).sort_values(by=['importance'],
                                                               ascending=False)
    plt.figure(figsize=(7, 10))
    sns.barplot(data = feimp, x='importance', y='feature')
    plt.title('Catboost Feature Importances')
    class_names = ['0','1']
    plot_confusion_matrix(confusion_matrix(y_val, y_val_class),
                          classes=class_names,
                          normalize=True,
                          title='Confusion Matrix')

