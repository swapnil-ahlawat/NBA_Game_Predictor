import pandas as pd
import numpy as np
import sklearn
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, log_loss
from sklearn.neural_network import MLPClassifier
from sklearn.svm import LinearSVC
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier

pd.set_option('display.max_columns', 500)
pd.set_option('display.max_rows', 500)


df = pd.read_csv('../data/NBAGameDataset.csv')

total = df.isnull().sum().sort_values(ascending=False)
percent = (df.isnull().sum()/df.isnull().count()).sort_values(ascending=False)
missing_data = pd.concat([total, percent], axis=1, keys=['Total', 'Percent'])
print("Missing Values:")
print(missing_data.head())

player_cols=['W/L','H Win Avg', 'V Win Avg', 'H Win Avg Last 8', 'V Win Avg Last 8']
for c in df.columns:
    temp=c
    c=c.split(' ')
    if len(c)>1 and c[1]=='Player':
        player_cols.append(temp)


df= df[player_cols]


# Correlation Matrix
# import matplotlib.pyplot as plt
# cmap = sns.diverging_palette(220, 10, as_cmap=True)
# corrmat = df.corr()
# f, ax = plt.subplots(figsize=(16, 12))
# sns.heatmap(corrmat, cmap=cmap, vmax=.8, square=True);

# print(abs(corrmat['W/L']).sort_values(ascending=False))

X = df.drop(columns=['W/L',
					'H Player AST Last 8', 'V Player AST Last 8', 'H Player PF', 'V Player PF', 'H Player TOV', 'V Player TOV', 'H Player STL Last 8', 'V Player STL Last 8', 'H Player 3P%', 'V Player 3P%', 'H Player +/- Last 8', 'V Player +/- Last 8',
                    'H Player +/-', 'V Player +/-'])

y = df['W/L']

# Hyperparameter Tuning Code 
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 42, shuffle = True)
# X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size = 0.2, random_state = 42, shuffle = True)
# scalar = StandardScaler()
# X_train = scalar.fit_transform(X_train)
# X_val =scalar.transform(X_val) 
# X_test = scalar.transform(X_test)

# grid_search=[]
# for i in [4, 8, 16]:
#     for j in range(2, 33, 2):
#         for k in range(2, 33, 2):
#             classifier_NN = MLPClassifier((i, j, k), max_iter = 5000, solver = 'sgd', alpha = 0.1, activation = 'relu', learning_rate='adaptive', random_state=42)
#             classifier_NN.fit(X_train, y_train)
#             y_pred_NN = classifier_NN.predict(X_val)
#             grid_search.append([i, j, k, accuracy_score(y_val, y_pred_NN)])
#             print(i, j, k, accuracy_score(y_val, y_pred_NN))
            
# mx_score=0
# mx_model=[]
# for l in grid_search:
#     if l[3]>mx_score:
#         mx_score=l[3]
#         mx_model=l
# print('Best Results:-{0}'.format(mx_model))

# grid_search=[]
# i=0.01
# while i<=10.0:
#     classifier_SV = LinearSVC(C = i, max_iter = 20000)
#     classifier_SV.fit(X_train, y_train)

#     y_pred_SV = classifier_SV.predict(X_val)
#     grid_search.append([i, accuracy_score(y_val, y_pred_SV)]) 
#     print(i, accuracy_score(y_val, y_pred_SV))
#     i*=3

# mx_score=0
# mx_model=[]
# for l in grid_search:
#     if l[1]>mx_score:
#         mx_score=l[1]
#         mx_model=l
# print('Best Results:-{0}'.format(mx_model))



# grid_search=[]
# i=0.01
# while i<=10.0:
#     classifier_SV = SVC(C = i, max_iter = 200000, kernel='rbf')
#     classifier_SV.fit(X_train, y_train)

#     y_pred_SV = classifier_SV.predict(X_val)
#     grid_search.append([i, accuracy_score(y_val, y_pred_SV)]) 
#     print(i, accuracy_score(y_val, y_pred_SV))
#     i*=3

# mx_score=0
# mx_model=[]
# for l in grid_search:
#     if l[1]>mx_score:
#         mx_score=l[1]
#         mx_model=l
# print('Best Results:-{0}'.format(mx_model))

# grid_search=[]
# for i in range(100, 601, 100):
#     for j in range(5, 31):
#         classifier_RF = RandomForestClassifier(n_estimators = i, max_depth = j, n_jobs= -1, random_state=42)
#         classifier_RF.fit(X_train, y_train)
#         y_pred_RF = classifier_RF.predict(X_val)
#         grid_search.append([i, j, accuracy_score(y_val, y_pred_RF)])
#         print(i, j, accuracy_score(y_val, y_pred_RF))

# mx_score=0
# mx_model=[]
# for l in grid_search:
#     if l[2]>mx_score:
#         mx_score=l[2]
#         mx_model=l
# print('Best Results:-{0}'.format(mx_model))


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 42, shuffle = True)
scalar = StandardScaler()
X_train = scalar.fit_transform(X_train)
X_test = scalar.transform(X_test)

#Neural Network
classifier_NN = MLPClassifier((16, 24, 4), max_iter = 5000, solver = 'sgd', alpha = 0.1, activation = 'relu', learning_rate='adaptive', random_state=42)
classifier_NN.fit(X_train, y_train)
y_pred_NN = classifier_NN.predict(X_test)
print("Accuracy on Neural Network: {0}".format(accuracy_score(y_test, y_pred_NN)))
print("Binary Cross-Entropy on Neural Network: {0}".format(log_loss(y_test, y_pred_NN)))

#Random Forest
classifier_RF = RandomForestClassifier(n_estimators = 200, max_depth = 13, n_jobs= -1, random_state=42)
classifier_RF.fit(X_train, y_train)
y_pred_RF = classifier_RF.predict(X_test)
print("Accuracy on Random Forest Classifier: {0}".format(accuracy_score(y_test, y_pred_RF)))
print("Binary Cross-Entropy on Random Forest Classifier: {0}".format(log_loss(y_test, y_pred_RF)))

#SVM
classifier_SV = LinearSVC(C = 0.1, max_iter = 20000)
classifier_SV.fit(X_train, y_train)
y_pred_SV = classifier_SV.predict(X_test)
print("Accuracy on SVM Classifier: {0}".format(accuracy_score(y_test, y_pred_SV)))
print("Binary Cross-Entropy on SVM Classifier: {0}".format(log_loss(y_test, y_pred_SV)))