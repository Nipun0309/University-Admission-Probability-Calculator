import sigmoid as s
def sigmoidGradient(z):
    #   sigmoidGradient(z) computes and returns the gradient of the sigmoid function
    #   evaluated at z. This should work regardless if z is a matrix or a
    #   vector. In particular, if z is a vector or matrix, it should return
    #   the gradient for each element.

    g = s.sigmoid(z)
    g = g * (1 - g)

    return g
