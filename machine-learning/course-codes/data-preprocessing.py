# Data Preprocessing Tools

## Importing libraries
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

"""## Importing the dataset"""

df = pd.read_csv('Data.csv') 
X = df.iloc[:, :-1].values # features
y = df.iloc[:, -1].values # dependable variable vector

"""## Processing missing data"""

from sklearn.impute import SimpleImputer
imputer = SimpleImputer(missing_values=np.nan, strategy='mean')
imputer.fit(X[:, 1:3]) # fits data and calculates missing values
X[:, 1:3] = imputer.transform(X[:, 1:3]) # inserts calculated missing values

"""## Encoding categorical data"""

from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
ct = ColumnTransformer(transformers=[('encoder', OneHotEncoder(), [0])], remainder='passthrough')
X = np.array(ct.fit_transform(X))

"""## Encoding dependent variable"""

from sklearn.preprocessing import LabelEncoder
le = LabelEncoder()
y = le.fit_transform(y)

"""## Splitting dataset into train and test sets"""

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=1)
# test_size ensures proper split, here 20% data goes into test
# random_state ensures reproducible split


"""## Feature scaling"""

from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
X_train[:, 3:] = sc.fit_transform(X_train[:, 3:])
X_test[:, 3:] = sc.transform(X_test[:, 3:])
