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

def flatten(w) -> list[list[float]] :
    """flattens a matrix to a 1 dimensional vector"""

def unflatten(w, shape) -> list[list[float]] :
    """transforms a single dimension vector into a matrix"""

class Network:
    def __init__(self) -> None:
        self.layers : list[Layer] = list()
        self.self_init()
        self.fitness = None
    
    def add(self, output_size : int, input_size : int = None, activation : callable = leakyRelu, w= np.array([])) -> None:
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
        self.add(2, 11, activation= sigmoid)
        # self.add(16)
        # self.add(2, activation= sigmoid)
        # self.add(2, activation= sigmoid)

    def flatten(self):
        """returns a combined vector of weights of the network"""
        return np.concatenate([layer.flatten() for layer in self.layers])

    def setWeights(self, w: list[float]):
        """Sets new weights to neural networks"""
        start = 0
        for l in self.layers:
            start += l.unflattenAndSet(w[start:])
        

class Layer:
    def __init__(self, input_size: int, output_size: int, weights: list[list[float]]= np.array([]), activation_function: callable = leakyRelu) -> None:
        self.input_size : int = input_size
        self.output_size : int = output_size
        self.weights = self.setWeights(weights)
        self.f_activation : callable = np.vectorize(activation_function)
        self.f_name = activation_function.__name__
        self.shape = self.weights.shape
        self.bias = random.random() * 2 - 1
    
    def mutateBias(self):
        if (random.uniform(0.0, 1.0) > 0.1):
            self.bias = self.bias * 1.5 if random.random() > 0.5 else self.bias * 0.5
        if (random.uniform(0.0, 1.0) > 0.1):
            self.bias = self.bias * -1
        
    def setBias(self, newbias):
        self.bias = newbias
    
    def getBias(self):
        return self.bias
    
    def setWeights(self, w) -> list[list[int]]:
        """Sets weights as the desired weights from input or random weights."""
        if (len(w) != 0):
            return w
        return self.randomWeights()
    
    def forward(self, input_matrix : list[list[float]]):
        """Performs a forward pass from the input matrix."""
        # check if the dimensions correspond
        # input_matrix should be in this form: [[float], [float], [float]...]
        if (input_matrix.shape[1] != self.input_size):
            raise ValueError("Input shape != weights' shape.\nForward function, Layer class.")
        f = np.matmul(input_matrix, self.weights)
        return self.f_activation(f + self.bias)

    def randomWeights(self):
        """Initialize the weights with the He initialization."""
        n = self.input_size
        return np.array([[random.normalvariate(mu=0, sigma= np.sqrt(2/n)) for _ in range(self.output_size)] for _ in range(self.input_size)])

    def flatten(self):
        """flattens the weights of this layer"""
        return self.weights.flatten()

    def unflattenAndSet(self, w):
        """unflattens the argument to the corresponding shape and sets the weights"""
        w = np.reshape(w[:np.product(self.shape)], self.shape)
        self.setWeights(w)
        return np.product(self.shape)
    
    def __repr__(self) -> str:
        return "Weights shape: {}, Activation: {}".format(self.weights.shape, self.f_name)

class GeneticNetwork:
    """Main class, used to manipulate agents in terms of their neural netowrk and perform genetic algorithm transofmations (fitness, selection, crossover and mutation)"""
    def __init__(self, population_size: int) -> None:
        self.agents : list[Network] = [Network() for _ in range(population_size)]
        self.pop_size = population_size
        
    def advance(self):
        """Runs the genetic algorithm on current agnets"""
        evaluation = self.evaluate()
        sorted_agents = self.select(evaluation)
        new_2_agents = self.crossover(sorted_agents[:2])
        mutated_agents = self.mutate(new_2_agents + sorted_agents)
        agents = sorted_agents[:2] + mutated_agents
        self.agents =  agents + [Network() for _ in range(self.pop_size - len(agents))]
        if (len(self.agents) != self.pop_size):
            raise ValueError("Agents != pop_size")

    def evaluate(self) -> list[(float, Network)]:
        """Evaluates agent performace, returns a lit of couples (score, network)"""
        # each drone will score itself upon dying.
        return [(n.fitness, n) for n in self.agents]
    
    def select(self, evaluation) -> list[Network]:
        """Method that returns 20% of the agents sorted by their score"""
        return [x[1] for x in sorted(evaluation, key= lambda x : x[0], reverse= False)][:int(0.2*self.pop_size)]

    def crossover(self, nets: list[Network]) -> list[Network]:
        """Method used to perform the crossover between 2 agents (networks)"""
        unflattened_weights = [n.flatten() for n in nets]
        if (len(unflattened_weights[0]) != len(unflattened_weights[1])):
            raise ValueError("Networks doesn't have the same number of neurones")
        for i in range(len(unflattened_weights[0])):
            if (random.random() > 0.5):
                unflattened_weights[0][i], unflattened_weights[1][i] = unflattened_weights[1][i], unflattened_weights[0][i]
        # slice_at = random.randint(a= 1, b= len(unflattened_weights[0])-1)
        # unflattened_weights = np.concatenate([unflattened_weights[i][:slice_at].tolist() + unflattened_weights[(i+1)%2][slice_at:].tolist() for i in range(2)])
        unflattened_weights = np.concatenate(unflattened_weights)
        start = 0
        length = 0
        for n in nets:
            length += len(n.flatten())
            n.setWeights(unflattened_weights[start:length])
            start += length
        return nets

    def mutate(self, agents: list[Network]) -> list[Network]:
        """Method used to perform a random mutation on a network"""
        for agent in agents:
            flattened = agent.flatten()
            if random.uniform(0.0, 1.0) <= 0.1:
                randint = random.randint(0,len(flattened)-1)
                # flattened[randint] = np.random.randn()
                if (random.random() > 0.5):
                    flattened[randint] = flattened[randint]*0.5 if (random.random() > 0.5) else flattened[randint]*1.5
                else:
                    flattened[randint] = flattened[randint] if (random.random() > 0.5) else flattened[randint]*-1
            agent.setWeights(flattened)
        return agents 

# def leakyRelu(numpy_2d_martrix):
#     a = 0.001
#     for i, arr in enumerate(numpy_2d_martrix):
#         numpy_2d_martrix[i] = [a*x if x < 0 else x for x in arr]
#     return numpy_2d_martrix

if __name__ == '__main__':
    n = Network()
    n.summary()
    print(n.forward(np.array([[1, 1, 1]])))