# Pandas is a software library written for the Python programming language for data manipulation and analysis.
import pandas as pd
# NumPy is a library for the Python programming language, adding support for large, multi-dimensional arrays and matrices, along with a large collection of high-level mathematical functions to operate on these arrays
import numpy as np
# Matplotlib is a plotting library for python and pyplot gives us a MatLab like plotting framework. We will use this in our plotter function to plot data.
import matplotlib.pyplot as plt
#Seaborn is a Python data visualization library based on matplotlib. It provides a high-level interface for drawing attractive and informative statistical graphics
import seaborn as sns
# Preprocessing allows us to standarsize our data
from sklearn import preprocessing
# Allows us to split our data into training and testing data
from sklearn.model_selection import train_test_split
# Allows us to test parameters of classification algorithms and find the best one
from sklearn.model_selection import GridSearchCV
# Logistic Regression classification algorithm
from sklearn.linear_model import LogisticRegression
# Support Vector Machine classification algorithm
from sklearn.svm import SVC
# Decision Tree classification algorithm
from sklearn.tree import DecisionTreeClassifier
# K Nearest Neighbors classification algorithm
from sklearn.neighbors import KNeighborsClassifier

# Constants
DATA_DIR = '/Users/fpj/Development/python/spacey/data/'
DATASET2 = 'dataset_part_2.csv'
DATASET3 = 'dataset_part_3.csv'

# Function to plot confusion matrix
def plot_confusion_matrix(y,y_predict):
    "this function plots the confusion matrix"
    from sklearn.metrics import confusion_matrix

    cm = confusion_matrix(y, y_predict)
    ax= plt.subplot()
    sns.heatmap(cm, annot=True, ax = ax); #annot=True to annotate cells
    ax.set_xlabel('Predicted labels')
    ax.set_ylabel('True labels')
    ax.set_title('Confusion Matrix'); 
    ax.xaxis.set_ticklabels(['did not land', 'land']); ax.yaxis.set_ticklabels(['did not land', 'landed']) 
    plt.show() 

data = pd.read_csv(DATASET2)
print(data.head())
X = pd.read_csv(DATASET3)
print(X.head())

# Create a NumPy arra from the column Class in data, by applying the method to_numpy()
Y = data['Class'].to_numpy()
# Standardize the data in X then reassign it to X
X = preprocessing.StandardScaler().fit(X).transform(X)
# Split the data into training and testing data
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=2)
#
# check the number of test samples
print('Number of test samples: ', Y_test.shape)

# Create a logistic regression object
parameters ={'C':[0.01,0.1,1],
             'penalty':['l2'],
             'solver':['lbfgs']}
#
lr = LogisticRegression()
# Create a grid search object with a cv = 10
logreg_cv = GridSearchCV(lr, parameters, cv=10, refit=True)
logreg_cv.fit(X_train, Y_train)
#
print("Tuned hyperparameters :(best parameters) ",logreg_cv.best_params_)
print("Accuracy :",logreg_cv.best_score_)

# Calculate the accuracy on the test data using the method score
print("LR\nTest accuracy: ", logreg_cv.score(X_test, Y_test))
# Let's look at the confusion matrix
yhat = logreg_cv.predict(X_test)
plot_confusion_matrix(Y_test, yhat)

# Create a support vector machine object
parameters ={'kernel':('linear', 'rbf', 'poly', 'rbf', 'sigmoid'),
             'C':np.logspace(-3, 3, 5),
             'gamma':np.logspace(-3, 3, 5)}
#
svm = SVC()
# Create a grid search object with a cv = 10
svm_cv = GridSearchCV(svm, parameters, cv=10, refit=True)
# Fit the model to the data
svm_cv.fit(X_train, Y_train)
#
print("SVM\nTuned hyperparameters :(best parameters) ", svm_cv.best_params_)
print("Accuracy :", svm_cv.best_score_)
# Calculate the accuracy on the test data using the method score
print("Test accuracy: ", svm_cv.score(X_test, Y_test))
# Let's look at the confusion matrix
yhat = svm_cv.predict(X_test)
plot_confusion_matrix(Y_test, yhat)

# Create a decisiton tree classifier
parameters = {'criterion': ['gini', 'entropy'],
     'splitter': ['best', 'random'],
     'max_depth': [2*n for n in range(1,10)],
     'max_features': ['log2', 'sqrt'],
     'min_samples_leaf': [1, 2, 4],
     'min_samples_split': [2, 5, 10]}

tree = DecisionTreeClassifier()
# Create a grid search object with a cv = 10
tree_cv = GridSearchCV(tree, parameters, cv=10, refit=True)
tree_cv.fit(X_train, Y_train)
#
print("DecisionTree\nTuned hyperparameters :(best parameters) ", tree_cv.best_params_)
print("Accuracy :", tree_cv.best_score_)
# Calculate the accuracy on the test data using the method score
print("Test accuracy: ", tree_cv.score(X_test, Y_test))
# Let's look at the confusion matrix
yhat = tree_cv.predict(X_test)
plot_confusion_matrix(Y_test, yhat)

# Create a k nearest neighbors classifier
parameters = {'n_neighbors': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
              'algorithm': ['auto', 'ball_tree', 'kd_tree', 'brute'],
              'p': [1, 2]}
KNN = KNeighborsClassifier()
# Create a grid search object with a cv = 10
knn_cv = GridSearchCV(KNN, parameters, cv=10, refit=True)
knn_cv.fit(X_train, Y_train)
#
print("KNN\nTuned hyperparameters :(best parameters) ", knn_cv.best_params_)
print("Accuracy :", knn_cv.best_score_)
# Calculate the accuracy on the test data using the method score
print("Test accuracy: ", knn_cv.score(X_test, Y_test))
# Let's look at the confusion matrix
yhat = knn_cv.predict(X_test)
plot_confusion_matrix(Y_test, yhat)

# Determine which method worked best
index = np.argmax([logreg_cv.best_score_, svm_cv.best_score_, tree_cv.best_score_, knn_cv.best_score_])
models = [logreg_cv, svm_cv, tree_cv, knn_cv]
print('Best performing model is \n',models[index].best_estimator_)
