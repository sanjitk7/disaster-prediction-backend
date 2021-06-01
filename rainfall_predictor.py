
# INDIAN RAINFALL

import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder
from sklearn import preprocessing
from sklearn import utils
from sklearn.model_selection import train_test_split
from sklearn import metrics
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_absolute_error
from sklearn.preprocessing import StandardScaler



# Read dataset
rainfall_df = pd.read_csv('Datasets/rainfall_india_1901-2017.csv')

# Deal with NaN values
rainfall_df.fillna(value = 0, inplace = True)

#Normalize the continuous values:
rainfall_df[['JAN',	'FEB',	'MAR', 'APR',	'MAY',	'JUN',	'JUL',	'AUG',	'SEP',	'OCT',	'NOV',	'DEC',	'ANNUAL',	'JF',	'MAM',	'JJAS',	'OND']] = StandardScaler().fit_transform(rainfall_df[['JAN',	'FEB',	'MAR', 'APR',	'MAY',	'JUN',	'JUL',	'AUG',	'SEP',	'OCT',	'NOV',	'DEC',	'ANNUAL',	'JF',	'MAM',	'JJAS',	'OND']])

# Split train and test sets
div_data = np.asarray(rainfall_df[['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']])

X = None; y = None
for i in range(div_data.shape[1]-3):
    if X is None: 
        X = div_data[:, i:i+3] # Three consecutive months
        y = div_data[:, i+3] # Next (fourth) month
    else:
        X = np.concatenate((X, div_data[:, i:i+3]), axis=0) # Three consecutive months
        y = np.concatenate((y, div_data[:, i+3]), axis=0) # Next (fourth) month
        
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=5)

# Perform Regression
rf = RandomForestRegressor(n_estimators = 200, max_depth=10)
rf.fit(X_train, y_train)

def predictor(my_array):
    y_pred = rf.predict(my_array) #array of 1 value
    return y_pred[0]

def get_mae():
    reg = LinearRegression()
    reg.fit(X_train, y_train)
    y_pred_reg = reg.predict(X_test)

    dec = DecisionTreeRegressor()
    dec.fit(X_train, y_train)
    y_pred_dec = dec.predict(X_test)

    clf = RandomForestRegressor(n_estimators=200, max_depth = 10, criterion='mse')
    clf.fit(X_train, y_train)
    y_pred_clf = clf.predict(X_test)

    xgb = XGBRegressor()
    xgb.fit(X_train, y_train)
    y_pred_xgb = xgb.predict(X_test)

    return [mean_absolute_error(y_test, y_pred_reg), mean_absolute_error(y_test, y_pred_dec), mean_absolute_error(y_test, y_pred_clf), mean_absolute_error(y_test, y_pred_xgb)]