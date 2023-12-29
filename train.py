#!/usr/bin/env python
# coding: utf-8

import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction import DictVectorizer
from sklearn.ensemble import RandomForestRegressor

import pickle

#import dataset
df = pd.read_csv('data/world_economic_indicators.csv')

#rename the column
df.rename(columns={"Country Name": "country_name"}, inplace=True)
df.rename(columns={"Country Code": "country_code"}, inplace=True)
df.rename(columns={"Year": "year"}, inplace=True)
df.rename(columns={"Personal remittances, received (% of GDP)": "personal_remittances"}, inplace=True)
df.rename(columns={"Unemployment, total (% of total labor force)": "unemployment"}, inplace=True)
df.rename(columns={"GDP (current US$)_x": "gdp_x"}, inplace=True)
df.rename(columns={"GDP growth (annual %)_x": "gdp_grow_x"}, inplace=True)
df.rename(columns={"GDP (current US$)_y": "gdp_y"}, inplace=True)
df.rename(columns={"GDP growth (annual %)_y": "gdp_grow_y"}, inplace=True)

del df['gdp_grow_y']
del df['gdp_y']

df.rename(columns={"gdp_x": "gdp"}, inplace=True)
df.rename(columns={"gdp_grow_x": "gdp_grow"}, inplace=True)

data = df[['country_name','country_code']]
dictionary = dict(zip(data['country_name'], data['country_code']))

df = df.drop(["country_name"], axis = 1)

#filling missing values with the mean of each group, the group is the nation
df['personal_remittances'] = df['personal_remittances'].fillna(df.groupby('country_code')['personal_remittances'].transform('mean'))
df['unemployment'] = df['unemployment'].fillna(df.groupby('country_code')['unemployment'].transform('mean'))
df['gdp'] = df['gdp'].fillna(df.groupby('country_code')['gdp'].transform('mean'))
df['gdp_grow'] = df['gdp_grow'].fillna(df.groupby('country_code')['gdp_grow'].transform('mean'))
df = df.fillna(0)

for v in ['gdp']: #loop per ogni colonna
    df[v] = np.log1p(df[v])

# # Splitting the Data

df_full_train, df_test = train_test_split(df, test_size=0.2, random_state=11)
df_train, df_val = train_test_split(df_full_train, test_size=0.25, random_state=11)

df_train = df_train.reset_index(drop=True)
df_val = df_val.reset_index(drop=True)
df_test = df_test.reset_index(drop=True)
df_full_train = df_full_train.reset_index(drop=True)

y_train = df_train.unemployment
y_val = df_val.unemployment
y_test = df_test.unemployment
y_full_train = df_full_train.unemployment

del df_train['unemployment']
del df_val['unemployment']
del df_test['unemployment']
del df_full_train['unemployment']

def rmse(y, y_pred):
    error = y - y_pred #calcolo errore tra i 2 array
    se = error **2 #quadrato della differenza
    mse = se.mean() #media della differenza
    return np.sqrt(mse) #radice del valore medio

# # THE MODEL:
#train
train_dicts = df_train.to_dict(orient='records')
dv = DictVectorizer(sparse=False)
X_train = dv.fit_transform(train_dicts)
#val
val_dicts = df_val.to_dict(orient='records')
X_val = dv.transform(val_dicts)
#ft
#train
dicts_ft = df_full_train.to_dict(orient='records')
dv = DictVectorizer(sparse = False)
X_full_train = dv.fit_transform(dicts_ft)
#test
dicts_test = df_test.to_dict(orient='records')
X_test = dv.transform(dicts_test)

model = RandomForestRegressor( n_estimators=201, 
                                max_depth=100,
                                min_samples_leaf=1,
                                random_state=1) 
model.fit(X_full_train, y_full_train)

y_pred = model.predict(X_test)
_rmse = rmse(y_test, y_pred)
print(_rmse)

#exporting the model

output_file = 'unemployment.bin'
with open(output_file, 'wb') as f_out: 
    pickle.dump((dv, model), f_out)