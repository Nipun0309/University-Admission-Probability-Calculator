import numpy as np
import nnCostFunction as nncf
import checkNeuralNetworkGrad as cnng
import predict as pr
from sklearn import metrics
from sklearn.model_selection import train_test_split
from joblib import dump
import os
from scipy.optimize import minimize
from sklearn import preprocessing

# obtaining path of the file directory
my_path = os.path.abspath(os.path.dirname(__file__))
# initializing hidden layer size and output layer size
hidden_layer_size = 10
num_labels = 1
## ================================================================
# initializing lists for storing the name of the colleges, for storing path of features data
# and admission status data of each corresponding college
all_statusfiles = []
colleges = []
all_featurefiles = []


## ================================================================

# A depth-first preorder traversal is done in 'my_path" and the necessary values are found and stored
for r, d, f in os.walk(my_path + '/College Data/'):
    colleges.append(d)
    for item in f:
        if 'Admissionstatus.csv' in item:
            all_statusfiles.append(os.path.join(r, item))
        elif 'Featuresdata.csv' in item:
            all_featurefiles.append(os.path.join(r, item))

collegelist = np.array(colleges[0])
num_of_colleges = len(collegelist)
collegelist = np.repeat(collegelist, 2)
# collegelist is duplicated and appended to the end of
# collegelist as the process is to be repeated for calculating
# optimized weights for dataset with IB Predicted and GPA Score

## ================================================================
# Based on the outer loop, the calculations, optimized weights for all the colleges are computed for dataset with
# either GPA Score or with GPA

# Based on inner loop, the the calculations, optimized weights for all the colleges are computed for dataset with
# ACT Score or SAT Score
for j in range(2):
    for i in range(len(all_featurefiles)):
        x = np.loadtxt(all_featurefiles[i], delimiter=",")
        if j == 1:
            x = np.delete(x, 1, 1)
        elif j == 0:
            x = np.delete(x, 2, 1)
        input_layer_size = x.shape[1]
        ## ================================================================
        # Preprocessing of data is done
        scaler = preprocessing.StandardScaler().fit(x)
        x = scaler.transform(x)
        abc = np.loadtxt(all_statusfiles[i])[np.newaxis]
        Y = abc.T
        x_train, x_test, y_train, y_test = train_test_split(x, Y, test_size=0.3)
        X = x_train
        y = y_train
        m = X.shape[0]
        Theta1 = np.random.rand(hidden_layer_size, input_layer_size + 1)
        Theta2 = np.random.rand(num_labels, hidden_layer_size + 1)
        nn_params = np.concatenate((Theta1.reshape(Theta1.size, order='F'), Theta2.reshape(Theta2.size, order='F')))
        lambda_reg = 0
        ## ================================================================
        # Checking Backpropagation
        cnng.checkNeuralNetworkGrad(lambda_reg)
        # Checking Backpropagation with Regularization
        lambda_reg = 0.01
        cnng.checkNeuralNetworkGrad(lambda_reg)
        ## ================================================================
        # The Neural Network is trained and optimized weights Theta 1 and Theta 2 are calculated

        maxiter = 100000
        myargs = (input_layer_size, hidden_layer_size, num_labels, X, y, lambda_reg)
        results = minimize(nncf.nnCostFunction, x0=nn_params, args=myargs,
                           options={'disp': True, 'maxiter': maxiter, 'ftol': 0}, method="L-BFGS-B", jac=True)

        nn_params = results.x
        Theta1 = np.reshape(nn_params[:hidden_layer_size * (input_layer_size + 1)],
                            (hidden_layer_size, input_layer_size + 1), order='F')
        Theta2 = np.reshape(nn_params[hidden_layer_size * (input_layer_size + 1):],
                            (num_labels, hidden_layer_size + 1), order='F')

        ## ================================================================
        # Area under the precision-recall curve is caclulated

        y_test_prob = pr.predict(Theta1, Theta2, x_test)[3]
        precision, recall, thresholds = metrics.precision_recall_curve(y_test, y_test_prob)
        auc = metrics.auc(recall, precision)
        aucarray = np.array([auc])

        ## ================================================================
        # Based on the inner loop and outer loop, the optimized weights calculated are stored in the approprtiate
        # folder
        if j == 1:
            if i % 2 == 0:
                IBPath = my_path + "/Optimized Weights for IB/" + collegelist[i] + "/" + "ACT"
            elif i % 2 != 0:
                IBPath = my_path + "/Optimized Weights for IB/" + collegelist[i] + "/" + "SAT"
            # If the folder does not exist, it's created
            if not os.path.exists(IBPath):
                os.makedirs(IBPath)

            np.savetxt(os.path.join(IBPath, 'Theta1.csv'), Theta1, delimiter=',')
            np.savetxt(os.path.join(IBPath, 'Theta2.csv'), Theta2, delimiter=',')
            np.savetxt(os.path.join(IBPath, 'Auc.csv'), aucarray)
            dump(scaler, os.path.join(IBPath, 'scaler_file.joblib'))
        elif j == 0:
            if i % 2 == 0:
                GPAPath = my_path + "/Optimized Weights for GPA/" + collegelist[i] + "/" + "ACT"
            elif i % 2 != 0:
                GPAPath = my_path + "/Optimized Weights for GPA/" + collegelist[i] + "/" + "SAT"
            # If the folder does not exist, it's created
            if not os.path.exists(GPAPath):
                os.makedirs(GPAPath)
            # scaling attributes, Area Under the Precision-Recall curve value
            # and the optimized weights are then stored
            np.savetxt(os.path.join(GPAPath, 'Theta1.csv'), Theta1, delimiter=',')
            np.savetxt(os.path.join(GPAPath, 'Theta2.csv'), Theta2, delimiter=',')
            np.savetxt(os.path.join(GPAPath, 'Auc.csv'), aucarray, )
            dump(scaler, os.path.join(GPAPath, 'scaler_file.joblib'))
            ## ================================================================
## ================================================================
