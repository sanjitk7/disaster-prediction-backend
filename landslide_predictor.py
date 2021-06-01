# GLOBAL LANDSLIDES

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

# Read Dataset
landslide_df = pd.read_csv('Datasets/NASA_Global_Landslide_Catalog.csv')

# Drop unwanted features
landslide_df = landslide_df.drop(['source_name', 'source_link','event_id', 'event_date','event_time', 'event_title', 'event_description', 'location_description','storm_name','photo_link', 'notes', 'event_import_source','event_import_id','country_code','submitted_date', 'created_date', 'last_edited_date','admin_division_name','gazeteer_closest_point', 'gazeteer_distance','injury_count'], axis = 1)

# Drop unknown categories

to_remove = landslide_df[ (landslide_df['landslide_category'] == 'unknown') ].index
landslide_df = landslide_df.drop(to_remove)
to_remove = landslide_df[(landslide_df['location_accuracy'] == 'unknown')].index
landslide_df = landslide_df.drop(to_remove)

# Replace or drop unknown/NaN values

landslide_df = landslide_df.dropna(subset=['location_accuracy', 'landslide_category','landslide_trigger','landslide_size','landslide_setting','country_name'])

# Determine feature and target vectors
X_features = list(landslide_df.columns)
X_features.remove('fatality_count')
X = landslide_df[X_features]
y = landslide_df['fatality_count']
y = y.fillna(y.median()) # deal with na

# Encoding of categorical data
categorical = []
for i in X_features:
    if landslide_df[i].dtype=="object":
        categorical.append(i)
label_maps = {}
for i in categorical:
    le = preprocessing.LabelEncoder().fit(X[i])
    X[i]=le.transform(X[i])
    d = dict(zip(le.classes_, le.transform(le.classes_)))
    label_maps[i] = d

# Train and test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.20)

# Perform regression
clf = RandomForestRegressor(n_estimators=150, max_depth = None, criterion='mse')
clf.fit(X_train, y_train)

def predictor(my_array):

    enc_array = [[]]
    print('MY ARRAY: ',my_array)
    labels = ['location_accuracy',	'landslide_category',	'landslide_trigger', 'landslide_size', 'landslide_setting', 'country_name',	'admin_division_population','longitude','latitude']
    i = 0
    for label in labels:
        if(label=='admin_division_population' or label=='longitude' or label=='latitude'):
            enc_array[0].append(float(my_array[i]))
            i += 1
        else:
            t = label_maps[label][my_array[i]]
            i += 1
            enc_array[0].append(t)
        
        print('ENCODED ARRAY: ',enc_array)

    y_pred = clf.predict(enc_array)
    return y_pred

def get_mae():
    reg = LinearRegression()
    reg.fit(X_train, y_train)
    y_pred_reg = reg.predict(X_test)

    dec = DecisionTreeRegressor()
    dec.fit(X_train, y_train)
    y_pred_dec = dec.predict(X_test)

    clf = RandomForestRegressor(n_estimators=150, max_depth = None, criterion='mse')
    clf.fit(X_train, y_train)
    y_pred_clf = clf.predict(X_test)

    xgb = XGBRegressor()
    xgb.fit(X_train, y_train)
    y_pred_xgb = xgb.predict(X_test)

    return [mean_absolute_error(y_test, y_pred_reg), mean_absolute_error(y_test, y_pred_dec), mean_absolute_error(y_test, y_pred_clf), mean_absolute_error(y_test, y_pred_xgb)]