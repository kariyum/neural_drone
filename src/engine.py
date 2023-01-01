# this file is for managing the game window
import pygame
import time
from functools import partial
import matplotlib.pyplot as plt

# local imports
from drone import Drone
from network import GeneticNetwork

POP_SIZE = 30
class Engine:
    def __init__(self, width, height):
        # basic inits
        pygame.init()
        pygame.display.set_caption("Drone brain")
        
        self.screen = pygame.display.set_mode((width, height))
        self.w = width
        self.h = height
        self.fn_create_drone = partial(Drone, self.screen)
        # self.drone = self.fn_create_drone()
        self.genetic = GeneticNetwork(population_size= POP_SIZE)
        self.drones = [self.fn_create_drone() for _ in range(POP_SIZE)]

    def run(self):
        clock = pygame.time.Clock()
        start_time = time.time()
        generation = 0
        history_1 = list()
        history_2 = list()
        game_on = True
        while game_on:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_on = False
                    # raise SystemExit

            for i, (network, drone) in enumerate(zip(self.genetic.agents, self.drones)):
                if (drone.update(network) == 1 and network.fitness == None):
                    # drone is out of screen and so is dead. -> get fitness
                    self.genetic.agents[i].fitness = time.time() - start_time
                    # print(time.time() - start_time)
                drone.draw()
            
            if (all([not x.inScreen() for x in self.drones])):
                # genetic do your thing
                # for n in self.genetic.agents:
                #     print(n.fitness)
                # print("------------------------------")
                print("Gen: {}".format(generation))
                fitness = [n.fitness for n in self.genetic.agents]
                print("Best performance: {}".format(max(fitness)))
                print("Average performance: {}".format(sum(fitness)/len(fitness)))
                history_1.append(sum(fitness)/len(fitness))
                history_2.append(max(fitness))
                self.genetic.advance()
                for d in self.drones:
                    d.revive()
                # reset network scores
                for i in range(len(self.genetic.agents)):
                    self.genetic.agents[i].fitness = None
                generation += 1
                time.sleep(0.3)
                start_time = time.time()
                
            pygame.display.flip()     
            clock.tick(75)
            self.screen.fill(0)
        plot_history(history_1, history_2)

def plot_history(history_1, history_2):
    plt.figure(figsize=(15, 8))
    plt.subplot(1, 2, 1)
    plt.title("Average performace")
    plt.ylim(0, max(history_2)*1.1)
    plt.plot(range(len(history_1)), history_1)
    plt.subplot(1, 2, 2)
    plt.title("Best performance")
    plt.ylim(0, max(history_2)*1.1)
    plt.plot(range(len(history_2)), history_2)
    plt.show()