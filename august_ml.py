# August2017

from sklearn import preprocessing
import numpy as np

data = np.random.rand(3)*10
print(data)

# Preprocess data before training
# Standardization of datasets is a common requirement for many machine learning estimators
# preprocessing.scale(X, axis=0, with_mean=True, with_std=True, copy=True)
X_scaled = preprocessing.scale(data, axis=0, with_mean=True, with_std=True, copy=True)
print(X_scaled)


