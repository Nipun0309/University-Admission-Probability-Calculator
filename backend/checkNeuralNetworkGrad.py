import numpy as np
import debugging as deb
import nnCostFunction as nncf
import computeNumericalGradient as cng
from decimal import Decimal
import sys

def checkNeuralNetworkGrad(lambda_reg):
    ## ================================================================
    #   checkNeuralNetworkGrad(lambda_reg) creates a small neural network to check the
    #   backpropagation gradients. It will output the analytical gradients
    #   produced by the backpropagation code and the numerical gradients (computed
    #   using computeNumericalGradient). These two gradient computations should
    #   result in very similar values.
    input_layer_size = 5
    hidden_layer_size = 10
    num_labels = 1
    m = 6
    Theta1 = deb.debugging(hidden_layer_size, input_layer_size + 1)
    Theta2 = deb.debugging(num_labels, hidden_layer_size + 1)
    X = deb.debugging(m, input_layer_size)
    y = np.random.randint(0, num_labels + 1, (m, num_labels))
    nn_params = np.concatenate((Theta1.reshape(Theta1.size, order='F'), Theta2.reshape(Theta2.size, order='F')))

    def costFunc(p):
        return nncf.nnCostFunction(p, input_layer_size, hidden_layer_size,
                                   num_labels, X, y, lambda_reg)
    _, grad = costFunc(nn_params)
    numgrad = cng.computeNumericalGradient(costFunc, nn_params)
    ## ================================
    # Relative difference between numerical and analytical gradient is calculated.
    # If the relative difference is greater than 1e-9, a warning is displayed and the program is terminated.
    diff = Decimal(np.linalg.norm(numgrad - grad)) / Decimal(np.linalg.norm(numgrad + grad))
    if diff > 1e-9:
        print("Error, relative difference is greater than 1e-9, check difference")
        sys.exit()
