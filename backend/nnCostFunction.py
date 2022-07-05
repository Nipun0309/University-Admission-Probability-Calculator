import numpy as np
import predict as pr
import sigmoidGradient as sg
def nnCostFunction(nn_params, input_layer_size, hidden_layer_size, num_labels, X, y, lambda_reg):
    # nnCostFunction (nn_params, input_layer_size, hidden_layer_size, num_labels, X, y, lambda_reg)
    # implements the neural network cost function.
    # It computes the cost and gradient of the neural network. The
    # parameters for the neural network are "unrolled" into the vector
    # nn_params and need to be converted back into the weight matrices.
    #   The returned parameter grad should be a "unrolled" vector of the
    #   partial derivatives of the neural network.

    Theta1 = np.reshape(nn_params[:hidden_layer_size * (input_layer_size + 1)],
                        (hidden_layer_size, input_layer_size + 1), order='F')
    Theta2 = np.reshape(nn_params[hidden_layer_size * (input_layer_size + 1):],
                        (num_labels, hidden_layer_size + 1), order='F')
    m = X.shape[0]
    z2, a1, a2, a3 = pr.predict(Theta1, Theta2, X)
    ## ================================
    #  Unregularized Cost function is calculated
    cost = np.sum((-y) * np.log(a3) - ((1 - y) * np.log(1 - a3)))
    J = (1.0 / m) * cost
    ## ================================
    #  Regularized Cost function is calculated
    sumOfTheta1 = np.sum(Theta1[:, 1:] ** 2)
    sumOfTheta2 = np.sum(Theta2[:, 1:] ** 2)
    J = J + ((lambda_reg / (2.0 * m)) * (sumOfTheta1 + sumOfTheta2))
    ## ================================
    # Backpropagation is implemented and thus the analytical gradients are calculated and unrolled into single vector
    delta3 = a3 - y
    delta2 = (np.dot(delta3, Theta2)) * np.column_stack((np.ones((z2.shape[0], 1)), sg.sigmoidGradient(z2)))
    delta2 = delta2[:, 1:]
    Theta2_grad = (np.dot(delta3.T, a2)) * (1 / m)
    Theta1_grad = (np.dot(delta2.T, a1)) * (1 / m)
    Theta2_grad = Theta2_grad + (
                (float(lambda_reg) / m) * np.column_stack((np.zeros((Theta2.shape[0], 1)), Theta2[:, 1:])))
    Theta1_grad = Theta1_grad + (
                (float(lambda_reg) / m) * np.column_stack((np.zeros((Theta1.shape[0], 1)), Theta1[:, 1:])))
    grad = np.concatenate(
        (Theta1_grad.reshape(Theta1_grad.size, order='F'), Theta2_grad.reshape(Theta2_grad.size, order='F')))
    ## ================================

    return J, grad
