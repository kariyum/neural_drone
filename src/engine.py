# this file is for managing the game window
import pygame
import time
from functools import partial

# local imports
from drone import Drone

fn_create_drone = partial(Drone, )
class Engine:
    def __init__(self, width, height):
        # basic inits
        pygame.init()
        pygame.display.set_caption("Drone brain")
        
        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        self.w = width
        self.h = height
        self.drone = Drone(screen= self.screen)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    raise SystemExit
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_z:
                        self.drone.left_acceleration = True
                    if event.key == pygame.K_e:
                        self.drone.right_acceleration = True
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_z:
                        self.drone.left_acceleration = False
                    if event.key == pygame.K_e:
                        self.drone.right_acceleration = False
            
            self.drone.update(actions= [[1, 1]])
            self.drone.draw()
            if ( not self.drone.inScreen()):
                self.drone = Drone(screen= self.screen)
                time.sleep(0.3)
            pygame.display.flip()     
            self.clock.tick(75)
            self.screen.fill(0)
            