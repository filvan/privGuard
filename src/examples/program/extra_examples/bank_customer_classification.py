import os
import seaborn as sns
import matplotlib.pyplot as plt
import tensorflow
sns.set(color_codes=True)

#from sklearn.pipeline import Pipeline
from sklearn.model_selection import cross_val_score, cross_val_predict
from sklearn.model_selection import train_test_split, StratifiedShuffleSplit
from sklearn.model_selection import StratifiedKFold
from sklearn.model_selection import GridSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_curve, confusion_matrix
from sklearn.preprocessing import StandardScaler, RobustScaler
#read data

def run(data_folder, **kwargs):
    pd = kwargs.get('pandas')
    np = kwargs.get('numpy')
    cross_validation = kwargs.get('cross_validation')
    lgb = kwargs.get('lgb')
    model_selection = kwargs.get('model_selection')
    metrics = kwargs.get('metrics')
    KFold = model_selection.KFold
    roc_auc_score = metrics.roc_auc_score

    df = pd.read_csv(os.path.join(data_folder, 'data.csv'))
    df=df.drop(['RowNumber','CustomerId','Surname'], axis=1)



    # df.groupby(by = 'Gender')

    # plot of age and exited
    # return df.drop(['RowNumber','ConsumerId','Surname','CreditScore','Geography','Gender','Tenure','Balance','NumOfProducts','HasCrCard','IsActiveMember','EstimatedSalary','ConsentUse', 'ConsentShare', 'ConsentSell', 'ConsentRetetention', 'ConsentCollection', 'ConsentRetention','GuardianConsent', 'RequestDeletion', 'RequestDisclosure', 'RequestInaccurate'],axis=1)
        # Negative Correlations with our Class (The lower our feature value the more likely it will be a fraud transaction)

    # plot of Salary and exited
    # return df.drop(['RowNumber','ConsumerId','Surname','CreditScore','Geography','Gender','Tenure','Balance','NumOfProducts','HasCrCard','IsActiveMember','Age','ConsentUse', 'ConsentShare', 'ConsentSell', 'ConsentRetetention', 'ConsentCollection', 'ConsentRetention','GuardianConsent', 'RequestDeletion', 'RequestDisclosure', 'RequestInaccurate'],axis=1)

    # plot of Tenure and exited
    #return df.drop(['RowNumber','ConsumerId','Surname','CreditScore','Geography','Gender','EstimatedSalary','Balance','NumOfProducts','HasCrCard','IsActiveMember','Age','ConsentUse', 'ConsentShare', 'ConsentSell', 'ConsentRetetention', 'ConsentCollection', 'ConsentRetention','GuardianConsent', 'RequestDeletion', 'RequestDisclosure', 'RequestInaccurate'],axis=1)


    #plot exited and not exited
    # return df[df.Exited==1].count().Exited
    plt.show()

    sex=pd.get_dummies(df['Gender'])
    country=pd.get_dummies(df['Geography'])

    df=pd.concat([df,country],axis=1)

    df = df.drop(columns = ['Gender', 'Geography', 'Spain'])
    df['Gender']=sex['Female']
    df.head()

    y = df.Exited.values
    x_data = df.drop(['Exited'], axis = 1)
    x=(x_data-np.min(x_data))/(np.max(x_data)-np.min(x_data)).values

    x_train, x_test, y_train, y_test = train_test_split(x,y, test_size = 0.2, random_state=42)

    x_train = x_train.T
    y_train = y_train.T
    x_test = x_test.T
    y_test = y_test.T


    def initialize(dimension):
        weight = np.full((dimension, 1), 0.01)
        bias = 0.0
        return weight, bias


    def sigmoid(z):
        y_head = 1 / (1 + np.exp(-z))
        return y_head


    def forwardBackward(weight, bias, x_train, y_train):
        # Forward

        y_head = sigmoid(np.dot(weight.T, x_train) + bias)
        loss = -(y_train * np.log(y_head) + (1 - y_train) * np.log(1 - y_head))
        cost = np.sum(loss) / x_train.shape[1]

        # Backward
        derivative_weight = np.dot(x_train, ((y_head - y_train).T)) / x_train.shape[1]
        derivative_bias = np.sum(y_head - y_train) / x_train.shape[1]
        gradients = {"Derivative Weight": derivative_weight, "Derivative Bias": derivative_bias}

        return cost, gradients


    def update(weight, bias, x_train, y_train, learningRate, iteration):
        costList = []
        index = []

        # for each iteration, update weight and bias values
        for i in range(iteration):
            cost, gradients = forwardBackward(weight, bias, x_train, y_train)
            weight = weight - learningRate * gradients["Derivative Weight"]
            bias = bias - learningRate * gradients["Derivative Bias"]

            costList.append(cost)
            index.append(i)

        parameters = {"weight": weight, "bias": bias}

        # print("iteration:",iteration)
        # print("cost:",cost)

        plt.plot(index, costList)
        plt.xlabel("Number of Iteration")
        plt.ylabel("Cost")
        plt.show()

        return parameters, gradients


    def predict(weight, bias, x_test):
        z = np.dot(weight.T, x_test) + bias
        y_head = sigmoid(z)

        y_prediction = np.zeros((1, x_test.shape[1]))

        for i in range(y_head.shape[1]):
            if y_head[0, i] <= 0.5:
                y_prediction[0, i] = 0
            else:
                y_prediction[0, i] = 1
        return y_prediction

    def logistic_regression(x_train,y_train,x_test,y_test,learningRate,iteration):
        dimension = x_train.shape[0]
        weight,bias = initialize(dimension)
        parameters, gradients = update(weight,bias,x_train,y_train,learningRate,iteration)
        y_prediction = predict(parameters["weight"],parameters["bias"],x_test)
        print("Manuel Test Accuracy: {:.2f}%".format((1 - np.mean(np.abs(y_prediction - y_test)))*100))

    logistic_regression(x_train,y_train,x_test,y_test,1,200)

    X=df.drop("Exited", axis = 1)
    y=df['Exited']

    pipeline = Pipeline([('std_scaler', StandardScaler()),
            ])

    pipeline.fit_transform(X)

    X_scaled = pd.DataFrame(pipeline.fit_transform(X), columns=X.columns)

    data_scaled=pd.concat([X_scaled,y],axis=1)
    data_scaled.head()

    X=data_scaled.drop('Exited',axis=1)
    y=data_scaled['Exited']

    x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    classifiers = {
        "LogisiticRegression": LogisticRegression(solver='lbfgs'),
        "KNearest": KNeighborsClassifier(),
        "Support Vector Classifier": SVC(gamma='scale'),
        "DecisionTreeClassifier": DecisionTreeClassifier(),
        "RandomForestClassifier": RandomForestClassifier(n_estimators=100)
    }

    for key, classifier in classifiers.items():
        classifier.fit(x_train, y_train)
        training_score = cross_val_score(classifier, x_train, y_train, cv=5)
        print("Classifiers: ", classifier.__class__.__name__, "Has a training score of"
     , round(training_score.mean(), 3) * 100, "% accuracy score")

    from sklearn.model_selection import GridSearchCV


    # Logistic Regression
    log_reg_params = {"penalty": ['l2'], 'C': [0.0001, 0.001, 0.01, 0.1, 1, 10, 100, 1000]}



    grid_log_reg = GridSearchCV(LogisticRegression(solver='lbfgs'), log_reg_params, cv=5)
    grid_log_reg.fit(x_train, y_train)
    # We automatically get the logistic regression with the best parameters.
    log_reg = grid_log_reg.best_estimator_


    # Support Vector Classifier
    svc_params = {'C': [0.5, 0.7, 0.9, 1], 'kernel': ['rbf', 'poly', 'sigmoid', 'linear']}
    grid_svc = GridSearchCV(SVC(gamma='scale'), svc_params,cv=5)
    grid_svc.fit(x_train, y_train)

    # SVC best estimator
    svc = grid_svc.best_estimator_

    # DecisionTree Classifier
    tree_params = {"criterion": ["gini", "entropy"], "max_depth": list(range(2,4,1)),
                  "min_samples_leaf": list(range(5,7,1))}
    grid_tree = GridSearchCV(DecisionTreeClassifier(), tree_params,cv=5)
    grid_tree.fit(x_train, y_train)

    # tree best estimator
    tree_clf = grid_tree.best_estimator_

    #Random forest
    param_grid = parameters = {'n_estimators': [100, 200, 400],
                  'max_features': ['log2', 'sqrt','auto'],
                  'criterion': ['entropy', 'gini'],
                  'max_depth': [10],
                  'min_samples_split': [30],
                  'min_samples_leaf': [1]
                 }

    grid_forest = GridSearchCV(RandomForestClassifier(n_estimators=100), param_grid, cv=5)
    grid_forest.fit(x_train, y_train)

    forest = grid_forest.best_estimator_

    log_reg_pred = cross_val_predict(log_reg, x_train, y_train, cv=5,
                                 method="decision_function")

    svc_pred = cross_val_predict(svc, x_train, y_train, cv=5,
                                 method="decision_function")

    tree_pred = cross_val_predict(tree_clf, x_train, y_train, cv=5)

    forest_pred = cross_val_predict(forest, x_train, y_train, cv=5)

    from sklearn.metrics import roc_auc_score

    d = {'Classifier': ['Logistic Regression', 'Support Vector Classifier', 'Decision Tree Classifier',
                        'Random Forest Classifier'],
         '(ROC AUC) Score': [roc_auc_score(y_train, log_reg_pred), roc_auc_score(y_train, svc_pred),
                             roc_auc_score(y_train, tree_pred), roc_auc_score(y_train, forest_pred)]}
    df = pd.DataFrame(data=d)

    df

    sns.set_style("white")

    log_fpr, log_tpr, log_thresold = roc_curve(y_train, log_reg_pred)
    svc_fpr, svc_tpr, svc_threshold = roc_curve(y_train, svc_pred)
    tree_fpr, tree_tpr, tree_threshold = roc_curve(y_train, tree_pred)
    forest_fpr, forest_tpr, forest_threshold = roc_curve(y_train, forest_pred)


    def graph_roc_curve_multiple(log_fpr, log_tpr, forest_fpr, forest_tpr, svc_fpr, svc_tpr, tree_fpr, tree_tpr):
        plt.figure(figsize=(10, 5))
        plt.title('ROC Curve \n 4 Classifiers', fontsize=18)
        plt.plot(log_fpr, log_tpr,
                 label='Logistic Regression Classifier Score: {:.4f}'.format(roc_auc_score(y_train, log_reg_pred)))
        plt.plot(svc_fpr, svc_tpr, label='Support Vector Classifier Score: {:.4f}'.format(roc_auc_score(y_train, svc_pred)))
        plt.plot(tree_fpr, tree_tpr,
                 label='Decision Tree Classifier Score: {:.4f}'.format(roc_auc_score(y_train, tree_pred)))
        plt.plot(forest_fpr, forest_tpr,
                 label='Random Forest Classifier Score: {:.4f}'.format(roc_auc_score(y_train, forest_pred)))
        plt.plot([0, 1], [0, 1], 'k--')
        plt.axis([-0.01, 1, 0, 1])
        plt.xlabel('False Positive Rate', fontsize=16)
        plt.ylabel('True Positive Rate', fontsize=16)
        plt.annotate('Minimum ROC Score of 50% \n (This is the minimum score to get)', xy=(0.5, 0.5), xytext=(0.6, 0.3),
                     arrowprops=dict(facecolor='#6E726D', shrink=0.05),
                     )
        plt.legend()


    graph_roc_curve_multiple(log_fpr, log_tpr, forest_fpr, forest_tpr, svc_fpr, svc_tpr, tree_fpr, tree_tpr)
    sns.set_style("white")
    plt.show()


    y_pred_log_reg = log_reg.predict(x_test)
    y_pred_forest = forest.predict(x_test)
    y_pred_svc = svc.predict(x_test)
    y_pred_tree = tree_clf.predict(x_test)



    log_reg_cf = confusion_matrix(y_test, y_pred_log_reg)
    forest_cf = confusion_matrix(y_test, y_pred_forest)
    svc_cf = confusion_matrix(y_test, y_pred_svc)
    tree_cf = confusion_matrix(y_test, y_pred_tree)

    plt.figure(figsize=(20,10))

    plt.suptitle("Confusion Matrixes",fontsize=24)
    plt.subplots_adjust(wspace = 0.4, hspace= 0.4)

    plt.subplot(2,2,1)
    plt.title("Logistic Regression Confusion Matrix")
    sns.heatmap(log_reg_cf,annot=True,cmap="Blues",fmt="d",cbar=False)

    plt.subplot(2,2,2)
    plt.title("Support Vector Machine Confusion Matrix")
    sns.heatmap(svc_cf,annot=True,cmap="Blues",fmt="d",cbar=False)

    plt.subplot(2,2,3)
    plt.title("Decision Tree Classifier Confusion Matrix")
    sns.heatmap(tree_cf,annot=True,cmap="Blues",fmt="d",cbar=False)

    plt.subplot(2,2,4)
    plt.title("Random Forest Confusion Matrix")
    sns.heatmap(forest_cf,annot=True,cmap="Blues",fmt="d",cbar=False)


    plt.show()

    from sklearn.metrics import roc_auc_score

    d = {'Classifier': ['Logistic Regression', 'Support Vector Classifier', 'Decision Tree Classifier',
                        'Random Forest Classifier'],
         '(ROC AUC) Score': [roc_auc_score(y_test, y_pred_log_reg), roc_auc_score(y_test, y_pred_svc),
                             roc_auc_score(y_test, y_pred_tree), roc_auc_score(y_test, y_pred_forest)]}
    roc_test = pd.DataFrame(data=d)

    roc_test

    from sklearn.decomposition import PCA

    pca=PCA(n_components=2)
    principalComponents = pca.fit_transform(data_scaled.drop('Exited', axis=1))
    principalDf = pd.DataFrame(data = principalComponents
                 , columns = ['principal component 1', 'principal component 2'])

    finalDf = pd.concat([principalDf, data_scaled[['Exited']]], axis = 1)
    finalDf.head(5)

    sample=finalDf[:1000]

    fig = plt.figure(figsize = (8,8))
    ax = fig.add_subplot(1,1,1)
    ax.set_xlabel('Principal Component 1', fontsize = 15)
    ax.set_ylabel('Principal Component 2', fontsize = 15)
    ax.set_title('2 Component PCA', fontsize = 20)


    targets = [0,1]
    colors = ['r', 'b']
    for target, color in zip(targets,colors):
        indicesToKeep = sample['Exited'] == target
        ax.scatter(sample.loc[indicesToKeep, 'principal component 1']
                   , sample.loc[indicesToKeep, 'principal component 2']
                   , c = color
                   , s = 50)
    ax.legend(targets)
    ax.grid()

    from keras import models
    from keras import layers
    from keras.optimizers import Adam, RMSprop
    from keras.metrics import categorical_crossentropy
    from keras import regularizers

    n_inputs = x_train.shape[1]

    model = models.Sequential()
    model.add(layers.Dense(32, activation='relu', input_shape=(n_inputs,)))
    model.add(layers.Dropout(0.2))
    model.add(layers.Dense(32, activation='relu'))
    model.add(layers.Dropout(0.2))
    model.add(layers.Dense(1, activation='sigmoid'))

    model.compile(optimizer='rmsprop', loss='binary_crossentropy', metrics=['acc'])
    history = model.fit(x_train, y_train, validation_split=0.2, batch_size=512, epochs=100, shuffle=True, verbose=2)
    keras_predictions = model.predict_classes(x_test, batch_size=200, verbose=0)


    cm = confusion_matrix(y_test, keras_predictions)
    actual_cm = confusion_matrix(y_test, y_test)
    labels = ['No Exited', 'Exited']

    fig = plt.figure(figsize=(16,8))

    fig.add_subplot(221)
    plt.title("Confusion Matrix \n keras")
    sns.heatmap(cm,annot=True,cmap="Blues",fmt="d",cbar=False)

    #fig.add_subplot(222)
    #plt.title("Confusion Matrix \n (with 100% accuracy)")
    #sns.heatmap(actual_cm,annot=True,cmap="Blues",fmt="d",cbar=False)

    plt.show()
    acc = history.history['acc']
    history_dict = history.history
    loss_values = history_dict['loss']
    val_loss_values = history_dict['val_loss']
    epochs = range(1, len(acc) + 1)
    plt.plot(epochs, loss_values, 'bo', label='Training loss')
    plt.plot(epochs, val_loss_values, 'b', label='Validation loss')
    plt.title('Training and validation loss')
    plt.xlabel('Epochs')
    plt.ylabel('Loss')
    plt.legend()
    plt.show()




