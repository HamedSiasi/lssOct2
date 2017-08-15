from sklearn.svm import SVR
import numpy as np

#X = numpy.sort (numpy.random.uniform(5, 10, size=10), axis=0)

#T= [[1],[2],[4],[6],[7],[8]]
#TIME = np.array(T) 
#Y = [2,4,8,12,14,16]
TT=[]

T=[[1498724242],[1498722423],[1498720603],[1498718785],[1498716966],[1498715172],[1498713351]]
print(T)

for i in range(len(T)):
	#print (   int(str(T[i][0])[5:])  )
	TT.append(   [int(str(T[i][0]))-1498694400]  )

print (TT)
TIME = np.array(TT) 
Y = [1420, 1212, 1006, 802, 598, 394, 190]
#1836
#1628
print (TIME)
print (Y)
########################################
# Fit regression model
#from sklearn.svm import SVR
#svr_rbf = SVR(kernel='rbf', C=1e3, gamma=0.1).fit(TIME, Y).predict(26061)
print "-- %d" %(1498726061-1496275200)
svr_lin = SVR(kernel='linear',C=0.01, gamma=0.01,epsilon=0.00001,tol=0.0001).fit(TIME, Y).predict(1498726061-1498694400)

#svr_poly = SVR(kernel='poly', C=1e3, degree=2).fit(TIME, Y).predict(8726061)
#P = model.fit(TIME, Y).predict(10)
#print (svr_rbf)
print "%f" %(svr_lin)
#print (svr_poly)