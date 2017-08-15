print __doc__

###############################################################################
# Generate sample data
import numpy as np

X = np.sort(10*np.random.rand(6, 1), axis=0)
y = np.sin(X).ravel()

###############################################################################
# Add noise to targets
#
###############################################################################
# Fit regression model
from sklearn.svm import SVR

svr_rbf = SVR(kernel='rbf', C=1e4, gamma=0.1)
#svr_lin = SVR(kernel='linear', C=1e4)
#svr_poly = SVR(kernel='poly', C=1e4, degree=2)
print (X)
print (y)
y_rbf = svr_rbf.fit(X, y).predict(X)
#print (y_rbf)
#y_lin = svr_lin.fit(X, y).predict(X)
#y_poly = svr_poly.fit(X, y).predict(X)

###############################################################################
# look at the results
#import pylab as pl
#pl.plot(X, y, c='k', label='data')
#pl.hold('on')
#pl.plot(X, y_rbf, c='g', label='RBF model')
#pl.plot(X, y_lin, c='r', label='Linear model')
#pl.plot(X, y_poly, c='b', label='Polynomial model')
#pl.xlabel('data')
#pl.ylabel('target')
#pl.title('Support Vector Regression')
#pl.legend()
#pl.show()