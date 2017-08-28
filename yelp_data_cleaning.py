# -*- coding: utf-8 -*-
"""
Created on Sun Aug 27 14:53:00 2017

@author: timothyyamaguchi
"""

import pandas as pd
import numpy as np

df = pd.read_csv('yelp_data.csv') # importing the dataset
df = df*1 # changing boolean variables to 1 and 0
#df_head = df.head()

"""
# If needed to fill in missing data
from sklearn.preprocessing import Imputer #bringing in modules to fill in missing data
imputer = Imputer(missing_values = 'NaN', strategy = 'mean', axis = 0) #identifying how to fill in the missing data
imputer = imputer.fit(X[:, 1:3]) #identifying where the missing data is
X[:, 1:3] = imputer.transform(X[:, 1:3]) #filling in the missing data
"""

# Separating out to binary variables
alcohol = pd.get_dummies(df['Business - Alcohol'])
attire = pd.get_dummies(df['Business - Attire'])
corkage = pd.get_dummies(df['Business - BYOB/Corkage'])
noise = pd.get_dummies(df['Business - Noise Level'])
smoking = pd.get_dummies(df['Business - Smoking'])
wifi= pd.get_dummies(df['Business - Wi-Fi'])

# Merging the dataframes back together
frames = [df, alcohol, attire, corkage, noise, smoking, wifi]
yelp_test = pd.concat(frames, axis=1)
#yelp_head = yelp_test.head()

# Removing the unnecessary columns
del yelp_test['Business - Alcohol']
del yelp_test['Business - Attire']
del yelp_test['Business - BYOB/Corkage']
del yelp_test['Business - Noise Level']
del yelp_test['Business - Smoking']
del yelp_test['Business - Wi-Fi']
yelp_test.fillna(0,inplace=True) # replacing all n/a datapoints to 0
#yelp_head = yelp_test.head()

# Cleaning the dataframee's columns
yelp_test.columns.values[30] = 'no_bar'
yelp_test.columns.values[34] = 'no_corkage'
yelp_test.columns.values[36] = 'free_corkage'
yelp_test.columns.values[37] = 'average_noise'
yelp_test.columns.values[41] = 'no_smoking'
yelp_test.columns.values[42] = 'outdoor_smoking'
yelp_test.columns.values[43] = 'yes_smoking'
yelp_test.columns.values[44] = 'free_wifi'
yelp_test.columns.values[45] = 'no_wifi'
yelp_test.columns.values[46] = 'paid_wifi'

# Exporting yelp_test for Excel Regression
yelp_test.to_csv('out.csv', sep=',')

# Creating X and Y variables for regression
X = yelp_test.drop('Business - Stars', axis = 1) # removing Y variable
X = X.drop('Business - Id', axis = 1) # removing index
X = X.drop('User - Id', axis = 1) # removing index
Y = yelp_test['Business - Stars']

# Removing dummy variables to avoid multicolinearity
X = X.drop('no_bar', axis = 1)
X = X.drop('formal', axis = 1)
X = X.drop('free_corkage', axis = 1)
X = X.drop('very_loud', axis = 1)
X = X.drop('yes_smoking', axis = 1)
X = X.drop('paid_wifi', axis = 1)

# Running the regression
import statsmodels.formula.api as smf

result = smf.OLS(Y, X.astype(float)).fit()
print result.params
print result.summary()

# Running the regression for users average rating
X_user = yelp_test.drop('User - Average Stars', axis = 1) # removing Y variable
X_user = X_user.drop('Business - Id', axis = 1) # removing index
X_user = X_user.drop('User - Id', axis = 1) # removing index
Y_user = yelp_test['User - Average Stars']

# Removing dummy variables to avoid multicolinearity
X_user = X_user.drop('no_bar', axis = 1)
X_user = X_user.drop('formal', axis = 1)
X_user = X_user.drop('free_corkage', axis = 1)
X_user = X_user.drop('very_loud', axis = 1)
X_user = X_user.drop('yes_smoking', axis = 1)
X_user = X_user.drop('paid_wifi', axis = 1)

# Running the regression
import statsmodels.formula.api as smf

result = smf.OLS(Y_user, X_user.astype(float)).fit()
print result.params
print result.summary()
