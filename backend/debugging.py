import numpy as np
def debugging(rows, cols):
    # debugging(rows, cols) Initialize the weights of cols as
    # incoming connections and rows as outgoing connections using a fixed
    # strategy, this will help later in debugging

    #   Note that data is to be set to a matrix of size(rows, cols)

    data = np.zeros((rows, cols))
    data = np.reshape(np.sin(range(data.size)), data.shape) / 10

    return data
