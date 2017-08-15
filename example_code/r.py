from sklearn import svm
import numpy as np
import matplotlib.pyplot as plt 

X = np.sort(10*np.random.rand(10,1),axis=0)
y = np.sin(2*X).ravel()

XX = np.sort(10*np.random.rand(10,1),axis=0)

model = svm.SVR(C=1000, epsilon=0.0001)
model.fit(X,y)

a = 1.5
b = 3
c = 4

print(a, model.predict([[a]]))
print(a, model.predict([[b]]))
print(a, model.predict([[c]]))
z = model.predict(XX)

plt.plot(X, y, label='true data')
plt.plot(XX, z, label='reg')
plt.legend()
plt.show()