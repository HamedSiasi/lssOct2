#!/usr/bin/python

import time
from sklearn import svm
import numpy as np
import matplotlib.pyplot as plt 

Y = []
TimeArray = []


start = time.time()
time.clock() 

global model
model = svm.SVR(kernel='rbf', C=1e4, gamma=0.01)


for num in range(0,20):
	TimeArray.append([time.time()-start])
	Y.append( np.sin(TimeArray[num]) )
	print(Y)
	print(TimeArray)
	##
	model.fit(TimeArray, Y)
	##
	time.sleep(0.1)


time.sleep(5)

X = np.sort( (time.time()-start)*(np.random.rand(20, 1)), axis=0 )
print(X)
P = model.predict(X)
print(P)

R = np.sin(X)
print(R)


import pylab as pl
pl.plot(TimeArray, Y, c='k', label='model')
pl.hold('on')
pl.scatter(X, P, c='g', label='prediction')
pl.scatter(X, R, c='r', label='real')
#pl.plot(X, y_lin, c='r', label='Linear model')
#pl.plot(X, y_poly, c='b', label='Polynomial model')
pl.xlabel('time(s)')
pl.ylabel('reading')
pl.title('Support Vector Regression')
pl.legend()
pl.show()