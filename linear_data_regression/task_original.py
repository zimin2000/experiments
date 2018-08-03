import json, csv
import dateutil.parser
import datetime

def fff(s):
    d = dateutil.parser.parse(s)
    return int(d.strftime("%s"))

def avg(X1, X2):
    V = {}

    for (k,v) in X1.items():
        if k not in V:
            V[k] = []
        V[k].append(v)

    for (k,v) in X2.items():
        if k not in V:
            V[k] = []
        V[k].append(v)

#    print len(V.keys())

    A = {}

    for k in V.keys():
        A[k] = sum(V[k]) / len(V[k])

    return A

J = json.loads(open("data/data2.json").read())

C = []
csv_reader = csv.reader(open("data/data1.csv"), delimiter=',')
for row in csv_reader:
    C.append(row)

#print len(C)

J2 = dict(map(lambda v: (int(v[0]), float(v[1])), J.items()))

C2 = dict(map(lambda v: (fff(v[0]), float(v[1])), C))

#print C2

AJ = avg(J2, C2)
print ("---------")
print (AJ)

X = list(AJ.keys())
Y = list(AJ.values())

print (Y)

import numpy as np
from sklearn import linear_model
from sklearn.metrics import mean_squared_error, r2_score

# Split the data into training/testing sets
X_train = np.array(X)
y_train = np.array(Y)

X_train = X_train[:,np.newaxis]

# Create linear regression object
regr = linear_model.LinearRegression()

# Train the model using the training sets
regr.fit(X_train, y_train)

# The coefficients
print('Coefficients: \n', regr.coef_)

B2 = regr.coef_[0]

yy=0
start=None
D = []
for x in sorted(X):
    if start is None:
        start = x
    else:
        yy = AJ[x]-AJ[start]
        print ("{} {}".format(x-start, yy/float(x-start)))
        D.append(yy/float(x-start))

B1 = np.array(D).mean()

X_a = np.array(X).mean()
Y_a = np.array(Y).mean()

for i in range(len(X)):
    print ("{},{} | {} | {}".format(X[i],Y[i], (X[i]-X_a)*B1+Y_a, (X[i]-X_a)*B2+Y_a))
