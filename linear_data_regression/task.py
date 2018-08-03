import json, csv
import dateutil.parser
from datetime import datetime, timezone

def parse_time(s):
    """ Converts timestamp to seconds since epoch.
    """

    dt = dateutil.parser.parse(s)
#    epoch_time = int((dt - datetime(1970, 1, 1, tzinfo=timezone.utc)).total_seconds())
    epoch_time = int(dt.replace(tzinfo=timezone.utc).timestamp())

    return epoch_time

def average_by_time(Xs):
    """ Combine list of arrays and average them grouping by timestamp. 
    """
    X_merged = {}

    for X in Xs:
        for (t,x) in X:
            if t not in X_merged: X_merged[t] = []
            X_merged[t].append(x)

    X_avg = {}

    for t in X_merged.keys():
        X_avg[t] = sum(X_merged[t]) / len(X_merged[t])

    return list(X_avg.items())

def read_json(name):
    """ Read in the JSON file and return list of pairs timestamp and value.
    """
    DATA = json.loads(open(name).read())

    return map(lambda v: (int(v[0]), float(v[1])), DATA.items())

def read_csv(name):
    """ Read in the CSV file and return list of pairs timestamp and value.
    """

#    DATA = []
#    for row in csv.reader(open(name), delimiter=','):
#        DATA.append((parse_time(row[0]), float(row[1])))
#
#    return DATA

    DATA = list(csv.reader(open(name), delimiter=','))

    return map(lambda v: (parse_time(v[0]), float(v[1])), DATA)


import numpy as np
from sklearn import linear_model

import warnings
warnings.filterwarnings(action="ignore", module="sklearn", message="^internal gelsd")

def linear_regression_sklearn(data):
    """ Fit linear regression model for the data. 
    """
# Split the data into training/testing sets
    dataset = np.array(data)

    X_train = dataset[:,0].reshape(-1,1)
    y_train = dataset[:,1]

# Create linear regression object
    regr = linear_model.LinearRegression()

# Train the model using the training sets
    regr.fit(X_train, y_train)

    return (regr.coef_[0], regr.intercept_)
    
def linear_regression_manual(data):
    """ My incorrect way to fit the data to liner model manually.
    """
    X_0 = None
    Y_0 = None

    S_x = 0
    S_y = 0

    DELTA = []

    dataset = sorted(data)

    for (x,y) in dataset:
        S_x += x
        S_y += y

        if X_0 is None:
            X_0 = x
            Y_0 = y
            continue

        dx = x - X_0
        dy = y - Y_0

        DELTA.append(dy/dx)

    a = np.array(DELTA).mean()

    x_avg = S_x / len(dataset) 
    y_avg = S_y / len(dataset) 

    return (a, y_avg - x_avg*a)

def linear_regression_manual2(data):
    """ Correct way to fit the data to liner model manually.
    """
    dataset = np.array(data)

    X = dataset[:,0]
    Y = dataset[:,1]

    X_avg = X.mean()
    Y_avg = Y.mean()

    X_cntr = X - X_avg
    Y_cntr = Y - Y_avg

    a = (X_cntr*Y_cntr).sum() / (X_cntr*X_cntr).sum()
    b = Y_avg - a*X_avg

    return (a, b)

def main():
    data = average_by_time([read_csv('sensor_data/sensor1.csv'), 
                            read_json('sensor_data/sensor2.json')])

    s1 = linear_regression_sklearn(data)

    s2 = linear_regression_manual(data)

    s3 = linear_regression_manual2(data)

    for i in range(len(data)):
        print("{},{} | {} | {} | {}".format(data[i][0], data[i][1], 
                                            s1[0]*data[i][0]+s1[1],
                                            s2[0]*data[i][0]+s2[1],
                                            s3[0]*data[i][0]+s3[1]))

if __name__ == "__main__":
    # execute only if run as a script
    main()
