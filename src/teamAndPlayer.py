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

# Correlation Matrix
# import matplotlib.pyplot as plt
# cmap = sns.diverging_palette(220, 10, as_cmap=True)
# corrmat = df.corr()
# f, ax = plt.subplots(figsize=(16, 12))
# sns.heatmap(corrmat, cmap=cmap, vmax=.8, square=True);

# print(abs(corrmat['W/L']).sort_values(ascending=False))

X = df.drop(columns=['Match Up', 'Game Date', 'W/L', 
                     'H Player FG% Last 8', 'H Player FG%', 'V Player FG% Last 8', 'V Player FG%',  
                     'H Player FG% Last 8', 'H Player FG%', 'V Player FG% Last 8', 'V Player FG%',
                     'H Player 3P% Last 8', 'H Player 3P%', 'V Player 3P% Last 8', 'V Player 3P%',
                     'H Player FT% Last 8', 'H Player FT%', 'V Player FT% Last 8', 'V Player FT%',
                     'H OREB Last 8', 'H OREB', 'V OREB Last 8', 'V OREB',
                     'H DREB Last 8', 'H DREB', 'V DREB Last 8', 'V DREB',
                     'H Player BLK Last 8', 'H Player BLK', 'V Player BLK Last 8', 'V Player BLK',
                     'H AST Last 8', 'H Player AST', 'V AST Last 8', 'V Player AST',
                     'H STL Last 8', 'H Player STL', 'V STL Last 8', 'V Player STL',
                     'H Player TOV Last 8', 'H Player TOV', 'V Player TOV Last 8', 'V Player TOV',
                     'H PF Last 8', 'H PF', 'V PF Last 8', 'V PF',
                     'H Player Pts Diff Avg', 'V Player Pts Diff Avg',
                     'H Player Pts Diff Avg Last 8', 'V Player Pts Diff Avg Last 8',
                     'H Player +/- Last 8', 'V Player +/- Last 8',
                     'H Player +/-', 'V Player +/-',
                     'H Player AST Last 8', 'V Player AST Last 8', 'H Player PF', 'V Player PF',
                     'H Player DREB','V Player DREB',    
                     'H TOV', 'V TOV',
                     'H Player STL Last 8', 'V Player STL Last 8', 
                     'H 3P%', 'V 3P%',
                     'H Player PF', 'V Player PF',
                    ])

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
classifier_NN = MLPClassifier((16, 10, 30), max_iter = 5000, solver = 'sgd', alpha = 0.1, activation = 'relu', learning_rate='adaptive', random_state=42)
classifier_NN.fit(X_train, y_train)
y_pred_NN = classifier_NN.predict(X_test)
print("Accuracy on Neural Network: {0}".format(accuracy_score(y_test, y_pred_NN)))
print("Binary Cross-Entropy on Neural Network: {0}".format(log_loss(y_test, y_pred_NN)))

#Random Forest
classifier_RF = RandomForestClassifier(n_estimators = 400, max_depth = 6, n_jobs= -1, random_state=42)
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