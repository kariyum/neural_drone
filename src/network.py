import random
import numpy as np

def leakyRelu(f):
    a = 0.001
    return a*f if f < 0 else f

def relu(f):
    return f if f > 0 else 0

def sigmoid():
    pass

class Network:
    def __init__(self):
        self.layers = list()
        pass

    def forward(self):
        pass
        
    def add(self, output_size, activation, input_size= None, w= None):
        if (input_size == None and len(self.layers) == 0):
            exit("Adding a layer without input_size as a first layer. Check add method, Network class.")
        # set input_size of this current layer the same as the output size of the last added layer
        in_s = self.layers[-1].shape[1]
        self.layers.append(Layer(input_size= in_s, output_size= output_size, weights= w))
        pass

class Layer:
    def __init__(self, input_size, output_size, weights= None, activation_function= leakyRelu):
        self.input_size = input_size
        self.output_size = output_size
        self.weights = self.setWeights(weights)
        self.f_activation = np.vectorize(activation_function)
    
    def setWeights(self, w):
        """Sets current weights as the desired weights from input."""
        if (w != None):
            return w
        return self.randomWeights()
    
    def forward(self, input_matrix):
        """activation is a function passed by argument and used as an activation function for this layer"""
        f = np.matmul(input_matrix, self.weights)
        return self.f_activation(f)

    def randomWeights(self):
        """Initialize the weights with the He initialization."""
        n = self.input_size
        return [[random.normalvariate(mu=0, sigma= np.sqrt(2/n)) for _ in range(self.output_size)] for _ in range(self.input_size)]

# def leakyRelu(numpy_2d_martrix):
#     a = 0.001
#     for i, arr in enumerate(numpy_2d_martrix):
#         numpy_2d_martrix[i] = [a*x if x < 0 else x for x in arr]
#     return numpy_2d_martrix


