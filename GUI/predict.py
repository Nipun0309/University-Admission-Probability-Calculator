import sigmoid as s
import numpy as np


def predict(Theta1, Theta2, X):
    m = X.shape[0]

    a1 = np.column_stack((np.ones((m, 1)), X))  # = a1
    z2 = np.dot(a1, Theta1.T)
    a2 = np.column_stack((np.ones((z2.shape[0], 1)), s.sigmoid(z2)))
    z3 = np.dot(a2, Theta2.T)
    a3 = s.sigmoid(z3)
    return z2, a1, a2, a3
