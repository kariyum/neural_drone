# this file is for managing the game window
import pygame

# local imports
from drone import Drone

class Engine:
    def __init__(self, width, height):
        # basic inits
        pygame.init()
        pygame.display.set_caption("Drone brain")
        
        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()

        self.drone = Drone(pygame.math.Vector2(800, 500), self.screen)

    def run(self):
        fl = False
        fr = False
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    raise SystemExit
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_z:
                        fl = True
                    if event.key == pygame.K_e:
                        fr = True
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_z:
                        fl = False

                    if event.key == pygame.K_e:
                        fr = False

            if (fr == False):
                self.drone.fr *= 0.95
            else:
                self.drone.fr += 0.02
                self.drone.fr = min(self.drone.fr, 0.5)
            if (fl == False):
                self.drone.fl *= 0.95
            else:
                self.drone.fl += 0.02
                self.drone.fl = min(self.drone.fl, 0.5)
            
            self.drone.update()
            self.drone.draw()
            pygame.display.flip()     
            self.clock.tick(75)
            self.screen.fill(0)
            