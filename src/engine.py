# this file is for managing the game window
import pygame
import time
from functools import partial

# local imports
from drone import Drone
from network import GeneticNetwork

POP_SIZE = 10
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
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    raise SystemExit

            for i, (network, drone) in enumerate(zip(self.genetic.agents, self.drones)):
                if (drone.update(network) == 1 and network.score == None):
                    # drone is out of screen and so is dead. -> get score
                    self.genetic.agents[i].score = time.time() - start_time
                    # print(time.time() - start_time)
                drone.draw()
            
            if (all([not x.inScreen() for x in self.drones])):
                # genetic do your thing
                for d in self.drones:
                    d.revive()
                for n in self.genetic.agents:
                    print(n.score)
                print("------------------------------")
                # reset network scores
                for i in range(len(self.genetic.agents)):
                    self.genetic.agents[i].score = None
                time.sleep(0.3)
                start_time = time.time()
            pygame.display.flip()     
            clock.tick(75)
            self.screen.fill(0)
            