import numpy as np
from sklearn.preprocessing import normalize

data = np.random.rand(5)
print(data)

normalized_data = data / np.linalg.norm(data)
print(normalized_data)

#normalized_data = normalize(x[:,np.newaxis], axis=0).ravel()
#print(normalized_data)

#Scale input vectors individually to unit norm (vector length).




#from sklearn.preprocessing import StandardScaler
#standardized_data = StandardScaler().fit_transform(data)
#print(standardized_data)
#print(data.reshape(-1,1))