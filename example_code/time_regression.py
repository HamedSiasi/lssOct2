#!/usr/bin/python

import time
from sklearn import svm
import numpy as np
import matplotlib.pyplot as plt 

X = []
T = []
TT = []
P = []

start = time.time()
time.clock() 

plt.axis([0, 100, -11, 11])
plt.ion()
model = svm.SVR(C=1000, epsilon=0.0001)

for num in range(0,50):
	T.extend([time.time()-start])
	X.extend( [10*np.sin(T[num])] )

	print(X)
	print(T)

	
	model.fit([T[num]],[X[num]])
	

	#print(P)


	#print(X)
	#print(T)
	#plt.scatter(T, X)
	plt.plot(T, X, label='True data')
	
	#plt.legend()
	plt.show()
	plt.pause(0.1)

#plt.legend()
for n in range(0,50):
	TT.extend( 100*np.random.rand(1,1)[0] )
	P.extend( [model.predict(TT[n])] )
	plt.scatter(TT, P, label='Learning machine prediction')
	plt.pause(0.1)
#plt.legend()