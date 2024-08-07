# this file is for managing the game window
import pygame
import time
from functools import partial
import matplotlib.pyplot as plt

# local imports
from drone import Drone
from network import GeneticNetwork

POP_SIZE = 50
class Engine:
    def __init__(self, width, height):
        # basic inits
        pygame.init()
        pygame.display.set_caption("Drone brain")
        
        self.font = pygame.font.Font(pygame.font.get_default_font(), 24)
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
        generation = 1
        history_1 = list()
        history_2 = list()
        game_on = True
        propeller_animation = dict()
        weights_address = set()
        gen_time = time.time()
        generation_text_surface = self.font.render(f'GEN {generation}', True, (255, 255, 255))
        generation_textRect = generation_text_surface.get_rect()
        generation_textRect.topleft = (self.w * 0.02, self.h * 0.9)
        
        best_fitness_text_surface = self.font.render(None, True, (255, 255, 255))
        best_fitness_textRect = best_fitness_text_surface.get_rect()
        best_fitness_textRect.topleft = (self.w * 0.02, self.h * 0.95)
        while game_on:
            self.screen.blit(generation_text_surface, generation_textRect)
            self.screen.blit(best_fitness_text_surface, best_fitness_textRect)
            frame_dtime = time.time()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_on = False
                    # raise SystemExit

            for i, (network, drone) in enumerate(zip(self.genetic.agents, self.drones)):
                if (drone.inScreen()):
                    if (drone.update(network, time.time() - frame_dtime) == 1 and network.fitness == None):
                        # drone is out of screen and so is dead. -> get fitness
                        self.genetic.agents[i].fitness = time.time() - start_time
                    drone.draw(propeller_animation)
            # print(len(propeller_animation))
            
            if (all([not x.inScreen() for x in self.drones])):
                gen_time = time.time()
                # print([network.flatten() for network in self.genetic.agents])
                # genetic do your thing
                # for n in self.genetic.agents:
                #     print(n.fitness)
                # print("------------------------------")
                print("Gen: {}".format(generation))
                if len(set([hex(id(network)) for network in self.genetic.agents])) != POP_SIZE:
                    print("Networks have same memory address {}".format(len(set([hex(id(network)) for network in self.genetic.agents]))))
                    raise ValueError("Networks have same memory address {}".format(len(set([hex(id(network)) for network in self.genetic.agents]))))
                fitness = [(n.fitness, n) for n in self.genetic.agents]
                best_fitness, best_network = max(fitness, key= lambda x : x[0])
                print("Best performance: {}, weights set from random: {}".format(best_fitness, best_network.randomWeights))
                print("Average performance: {}".format(sum([s[0] for s in fitness])/len(fitness)))
                history_1.append(sum([s[0] for s in fitness])/len(fitness))
                history_2.append(best_fitness)
                # genetic algorithm iteration
                self.genetic.advance(generation)
                for d in self.drones:
                    d.revive()
                # reset network scores
                for i in range(len(self.genetic.agents)):
                    self.genetic.agents[i].fitness = None
                generation += 1
                generation_text_surface = self.font.render(f'GEN {generation}', True, (255, 255, 255))
                best_fitness_text_surface = self.font.render(f'Best {max(history_2):.2f} seconds at GEN {history_2.index(max(history_2)) + 1}', True, (255, 255, 255))
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