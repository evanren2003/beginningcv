from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import RidgeClassifier
from sklearn.linear_model import SGDClassifier
from sklearn.linear_model import Perceptron
from sklearn.svm import SVC
from sklearn.svm import LinearSVC

from sklearn.datasets import load_digits, load_iris, load_breast_cancer, load_wine
from sklearn.datasets import load_boston
from sklearn.model_selection import train_test_split
from sklearn.metrics import plot_confusion_matrix
# matplotlib 3.3.1
from matplotlib import pyplot

import numpy as np

#scalers
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MaxAbsScaler
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import RobustScaler
from sklearn.preprocessing import quantile_transform
from sklearn.preprocessing import power_transform
from sklearn.preprocessing import Normalizer
from sklearn.preprocessing import QuantileTransformer

#lol not gonna change the variable name each time
boston = load_boston()
bostonX = boston.data
bostonY = boston.target
for i in range(len(bostonY)):
    # bostonY[i] = bostonY[i]//10, changing to //5 made it less accurate
    bostonY[i] = bostonY[i]//4
    #the value is already divided by 10,000 or 100,000 or whatever it is
# print(max(bostonY), min(bostonY))

### below is data where i have bostonY[i]//10 not //4
#with 4, the average accuracy without scaling decreases to ~50 something percent

# scaler = StandardScaler()
# scaler.fit(bostonX)
# scaledX = scaler.transform(bostonX)
#Correct: 112, Incorrect: 40, % Correct:  0.74
#this did not actually improve the prediction

# transformer = MaxAbsScaler().fit(bostonX)
# transformer.transform(bostonX)
#Correct: 114, Incorrect: 38, % Correct:  0.75
#also did not really do anything

# scaler = MinMaxScaler()
# scaler.fit(bostonX)
# scaledX = scaler.transform(bostonX)
#Correct: 111, Incorrect: 41, % Correct:  0.73

# rng = np.random.RandomState(0)
# bostonX = np.sort(rng.normal(loc=0.5, scale=0.25, size=(25, 1)), axis=0)
# qt = QuantileTransformer(n_quantiles=12,random_state=0)
# scaledX = qt.fit_transform(bostonX)
# this one didnt work

# transformer =  RobustScaler().fit(bostonX)
# scaledX = transformer.transform(bostonX)
# Correct: 107, Incorrect: 45, % Correct:   0.7

# scaledX = power_transform(bostonX, method = 'box-cox')
# also didnt work

# transformer = Normalizer().fit(bostonX)
# scaledX = transformer.transform(bostonX)
#Correct: 92, Incorrect: 60, % Correct:  0.61
#the rest didnt do anything, but this one made it worse

trainX, testX, trainY, testY = train_test_split(
    bostonX, bostonY, test_size = 0.3, shuffle = True
)

quantile_transformer = QuantileTransformer(random_state=0)
trainX = quantile_transformer.fit_transform(trainX)
testX = quantile_transformer.transform(testX)
#ok so this actually made it worse D:
#averaged somewhere around 45%

### digits dataset:
# classifier = LogisticRegression(max_iter = 10000)
# Correct: 522, Incorrect: 18, % Correct:  0.97

# classifier = RidgeClassifier(max_iter = 10000)
# Correct: 509, Incorrect: 31, % Correct:  0.94

# classifier = SGDClassifier(max_iter = 10000)
# Correct: 514, Incorrect: 26, % Correct:  0.95
########## to do: look at the different loss functions

# classifier = Perceptron(max_iter = 10000)
# Correct: 488, Incorrect: 52, % Correct:   0.9

# classifier = SVC(max_iter = 10000)
# Correct: 529, Incorrect: 11, % Correct:  0.98
########## to do: look at the different kernels

# classifier = LinearSVC(max_iter = 10000)
# Correct: 516, Incorrect: 24, % Correct:  0.96 (ranged from 0.94 to 0.96)
#keeps giving Liblinear failed to converge, increase the number of iterations.

######## to do: experiment with different data sets

#iris dataset:
#classifier = LogisticRegression(max_iter = 10000)
# Correct: 40, Incorrect: 5, % Correct:  0.89
# Correct: 44, Incorrect: 1, % Correct:  0.98

#breast cancer dataset:
# classifier = LogisticRegression(max_iter = 10000)
# Correct: 163, Incorrect: 8, % Correct:  0.95

#wine dataset:
# classifier = LogisticRegression(max_iter = 10000)
# Correct: 52, Incorrect: 2, % Correct:  0.96

#to do: use the regression dataset for boston housing
# classifier = LogisticRegression(max_iter = 10000)
# Correct: 111, Incorrect: 41, % Correct:  0.73
#i think a lot of them hit iteraiton limit

classifier = LogisticRegression(max_iter = 10000)

classifier.fit(trainX, trainY)
preds = classifier.predict(testX)

correct = 0
incorrect = 0
for pred, gt in zip(preds, testY):
    if pred == gt: correct += 1
    else: incorrect += 1
print(f"Correct: {correct}, Incorrect: {incorrect}, % Correct: {correct/(correct + incorrect): 5.2}")

plot_confusion_matrix(classifier, testX, testY)
pyplot.show()
