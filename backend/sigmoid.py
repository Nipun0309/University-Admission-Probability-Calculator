import numpy as np
def sigmoid(z):
    # sigmoid(z) computes and returns the sigmoid (activation function) of z.
    g = np.zeros(z.shape)
    g = 1 / (1 + np.exp(-z))

    return g
