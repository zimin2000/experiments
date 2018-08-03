import json, csv, os
import pandas as pd
import numpy as np

from sklearn import linear_model

import warnings
warnings.filterwarnings(action="ignore", module="sklearn", message="^internal gelsd")

def average_by_time(Xs):
    """ Combine list of arrays and average them grouping by timestamp. 
    """

    return pd.concat(Xs).groupby(["ts"], as_index=False).mean()

def read_json(name):
    """ Read in the JSON file and return list of pairs timestamp and value.
    """

    JDATA = json.load(open(name))

    DATA = pd.DataFrame(list(JDATA.items()), columns=["ts", "value"])

    DATA['ts']  = pd.to_datetime(DATA['ts'], unit='s')

    return DATA

def read_csv(name):
    """ Read in the CSV file and return list of pairs timestamp and value.
    """

    DATA = pd.read_csv(open(name), names=["ts", "value"])

    DATA['ts'] = pd.to_datetime(DATA['ts'])

    return DATA

def linear_regression_sklearn(data):
    """ Fit linear regression model for the data. 
    """
    dataset = data.values

    X_train = dataset[:,0].reshape(-1,1)
    y_train = dataset[:,1]

    regr = linear_model.LinearRegression()

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

    data.sort_values(by='ts')

    for i, (x,y) in data.iterrows():

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

    X_avg = S_x / len(data) 
    Y_avg = S_y / len(data) 

    return (a, Y_avg - X_avg*a)

def linear_regression_manual2(data):
    """ Correct way to fit the data to liner model manually.
    """
    X = data['ts']
    Y = data['value']

    X_avg = X.mean()
    Y_avg = Y.mean()

    X_cntr = X - X_avg
    Y_cntr = Y - Y_avg

    a = (X_cntr*Y_cntr).sum() / (X_cntr*X_cntr).sum()
    b = Y_avg - a*X_avg

    return (a, b)

def main():

    DIR = "data"
    IN = []

    for fn in os.listdir(DIR):
        fname = os.path.join(DIR, fn)

        p, e = os.path.splitext(fn)
        if e == ".csv":     d = read_csv(fname)
        elif e == ".json":  d = read_json(fname)

        # Convert time to seconds.
        d['ts'] = d['ts'].astype('int64') // 1e9

        IN.append(d)

    DATA = average_by_time(IN)

    RESULT = pd.DataFrame()

    (a, b) = linear_regression_sklearn(DATA)
    RESULT['sklearn'] = a * DATA['ts'] + b

    (a, b) = linear_regression_manual(DATA)
    RESULT['manual'] = a * DATA['ts'] + b

    (a, b) = linear_regression_manual2(DATA)
    RESULT['manual2'] = a * DATA['ts'] + b

    print(pd.concat([DATA, RESULT], axis=1))

if __name__ == "__main__":
    # execute only if run as a script
    main()
