from multiprocessing.pool import ThreadPool
from network import GeneticNetwork
from PIL import Image
from os import listdir

POP_SIZE = 30
genetic = GeneticNetwork(population_size= POP_SIZE)
import numpy as np
import matplotlib.pyplot as plt

d = dict()

for classe in range(10):
    path = 'C:/Users/S B S/Documents/#currentWork/dataset/train/'+str(classe)
    l = listdir(path)[:100]
    img_arr = [Image.open(f"{path}/{x}") for x in l]
    # print(img_arr[0])
    print(f"classe {classe} {len(l)} images.")
    # input_vector = np.array(img_arr[0]).flatten()
    d[classe] = [np.array(i).flatten() for i in img_arr]
    # plt.figure(figsize=(10, 10))
    # for i, x in enumerate(l):
    #     plt.subplot(5, 5, i+1)
    #     plt.title(classe)
    #     plt.axis('off')
    #     plt.imshow(Image.open(path+'/'+x))
    # plt.show()
def getPerformance(d, mlp, i):
    performance = 0
    for c in d.keys():
        for x in d[c]:
            output = mlp.forward([x])
            predicted_number = np.argmax(output)
            if (predicted_number == c):
                performance += 1
    mlp.fitness = performance
    print(f"Agent {i} : {performance}")
    return performance

pool = ThreadPool(processes= 8)
for gen in range(10000):
    perf = list()
    threads = []
    for i, mlp in enumerate(genetic.agents):
        threads.append(pool.apply_async(getPerformance, (d, mlp, i)))
    
    for thread in threads:
        perf.append(thread.get())
    
    print(f"Avg performance {sum(perf)/len(perf)}")
    genetic.advance(gen)

