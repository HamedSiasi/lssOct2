from sklearn import preprocessing
import numpy as np

data = np.random.rand(5)*10
print(data)

X_scaled = preprocessing.scale(data)
print(X_scaled)
X_normalized = preprocessing.normalize(data, norm='l2')
print(X_normalized)
normalized_data = data / np.linalg.norm(data)
print(normalized_data)