import random
import numpy as np

def leakyRelu(f: float) -> float:
    a = 0.001
    return a*f if f < 0 else f

def relu(f: float) -> float:
    return f if f > 0 else 0

def sigmoid(f: float) -> float:
    return 1/(1+np.exp(-f))

def identity(f: float) -> float:
    return f

class Network:
    def __init__(self) -> None:
        self.layers : list[Layer] = list()
        self.self_init()
    
    def add(self, output_size : int, input_size : int = None, activation : callable = leakyRelu, w= None) -> None:
        if (input_size == None and len(self.layers) == 0):
            raise ValueError("Adding a layer without input_size as a first layer. Check add method, Network class.")
        # set input_size of this current layer the same as the output size of the last added layer
        in_s = input_size if len(self.layers) == 0 else self.layers[-1].output_size # this will ignore the input_size argument if it's not first layer and even if input_size != None
        self.layers.append(Layer(input_size= in_s, output_size= output_size, weights= w, activation_function= activation))

    def forward(self, input_matrix) -> list[list[float]]:
        """This method will perform a forward pass on the network (layers) and returns the result"""
        layer_input = np.array(input_matrix).copy()
        for layer in self.layers:
            layer_input = layer.forward(layer_input)
        return layer_input
    
    def summary(self) -> None:
        """This method prints the network architecture."""
        for i, layer in enumerate(self.layers):
            print("Layer {}: {}".format(i+1, layer))

    def self_init(self):
        self.add(12, 4, activation= leakyRelu)
        self.add(24)
        self.add(2, activation= sigmoid)

class Layer:
    def __init__(self, input_size: int, output_size: int, weights: list[list[float]]= None, activation_function: callable = leakyRelu) -> None:
        self.input_size : int = input_size
        self.output_size : int = output_size
        self.weights = self.setWeights(weights)
        self.f_activation : callable = np.vectorize(activation_function)
        self.f_name = activation_function.__name__
    
    def setWeights(self, w) -> list[list[int]]:
        """Sets weights as the desired weights from input or random weights."""
        if (w != None):
            return w
        return self.randomWeights()
    
    def forward(self, input_matrix : list[list[float]]):
        """Performs a forward pass from the input matrix."""
        # check if the dimensions correspond
        # input_matrix should be in this form: [[float], [float], [float]...]
        if (input_matrix.shape[1] != self.input_size):
            raise ValueError("Input shape != weights' shape.\nForward function, Layer class.")
        f = np.matmul(input_matrix, self.weights)
        return self.f_activation(f)

    def randomWeights(self):
        """Initialize the weights with the He initialization."""
        n = self.input_size
        return np.array([[random.normalvariate(mu=0, sigma= np.sqrt(2/n)) for _ in range(self.output_size)] for _ in range(self.input_size)])

    def __repr__(self) -> str:
        return "Weights shape: {}, Activation: {}".format(self.weights.shape, self.f_name)

class GeneticNetwork:
    """Main class, used to manipulate agents in terms of their neural netowrk and perform genetic algorithm transofmations (fitness, selection, crossover and mutation)"""
    def __init__(self, population_size: int) -> None:
        self.agents : list[Network] = [Network() for _ in range(population_size)]
    
    def evaluate(self):
        """Evaluates agent performace"""

    def select(self):
        """Method that aims to select best of current agents"""
    
    def crossover(self):
        """Method used to perform the crossover between 2 agents (networks)"""

    def mutate(self):
        """Method used to perform a random mutation on a network"""

# def leakyRelu(numpy_2d_martrix):
#     a = 0.001
#     for i, arr in enumerate(numpy_2d_martrix):
#         numpy_2d_martrix[i] = [a*x if x < 0 else x for x in arr]
#     return numpy_2d_martrix

if __name__ == '__main__':
    n = Network()
    n.summary()
    print(n.forward(np.array([[1, 1, 1]])))