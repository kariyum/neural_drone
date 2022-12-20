import pygame
import math
import random
class Propeller:
    def __init__(self, src, pos):
        self.pos = pos
        self.size = pygame.math.Vector2(20, 5)
        self.image = pygame.transform.scale(pygame.image.load(src), self.size)
        self.screen = screen
        self.rotated_image = pygame.transform.rotate(self.image, 0)
        self.rotated_image_rect = self.rotated_image.get_rect(center = self.pos)
    def draw(self):
        self.screen.blit(self.rotated_image, self.rotated_image_rect)
    
def degToRad(deg):
    return deg * math.pi / 180

def radToDeg(rad):
    return rad * 180 / math.pi
class Drone:
    def __init__(self, src, pos, screen):
        # src for image source
        self.size = pygame.math.Vector2(100, 50)
        self.image = pygame.transform.scale(pygame.image.load(src), self.size)
        self.rotated_image = pygame.transform.rotate(self.image, 0)
        self.pos = pygame.math.Vector2(pos.x, pos.y)
        self.rotated_image_rect = self.rotated_image.get_rect(center = self.pos)
        self.screen = screen
        self.friction = 0.05
        self.gravity = 0.5
        self.radius = 1/2
        self.mass = 1
        self.phiv = 0
        self.phi = 0
        self.vx = 0
        self.vy = 0
        self.fl = 0
        self.fr = 0
        self.l = list()
    def draw(self):
        self.screen.blit(self.rotated_image, self.rotated_image_rect)
        # self.screen.blit(self.image, self.image.get_rect())
        # self.screen.blit(self.rotated_image, self.pos)

    def update(self):
        self.update_forces()
    
    def update_forces(self):
        self.updateFR()
        self.updateFL()
        self.updatePhi()
        self.ax = (self.getFL() + self.getFR()) / self.mass * math.sin(self.getPhi())
        # self.ax += (self.getFL() + self.getFR())**2 * self.radius / self.mass * math.cos(self.getPhi()) 
        self.ay = (self.getFL() + self.getFR()) / self.mass * math.cos(self.getPhi()) - self.gravity / self.mass 
        # self.ay += (self.getFL() + self.getFR())**2 * self.radius / self.mass * - math.sin(self.getPhi()) 
        # print("ax = {}, ay = {}".format(self.ax, self.ay))
        # ..
        self.vx = self.vx * (1 - self.friction) + self.ax
        self.vy = self.vy * (1 - self.friction) + self.ay
        # print("vx = {}, vy = {}".format(self.vx, self.vy))
        # ..
        vx = self.vx - 0.5 * self.ax
        self.pos.x = self.pos.x + vx
        # print(self.phi)
        # ..
        vy = self.vy - 0.5 * self.ay
        self.pos.y = self.pos.y - vy
        self.rotated_image = pygame.transform.rotate(self.image, -radToDeg(self.getPhi()))
        self.rotated_image_rect = self.rotated_image.get_rect(center = self.pos)
        # print(self.vx, self.vy)
        self.l.append((self.vx, self.vy))
    
    def getPhi(self):
        return degToRad(self.phi)
    
    def getFL(self):
        # return random.random()
        return self.fl

    def getFR(self):
        # return random.random()
        return self.fr

    def updateFL(self):
        pass
    
    def updateFR(self):
        pass

    def updatePhi(self):
        self.phia = (self.getFL() - self.getFR()) * self.radius
        self.phiv = self.phiv * 0.975 + self.phia
        self.phi = self.phi + self.phiv
        pass
    
pygame.init()
# load and set the logo
pygame.display.set_caption("Genetic Neural Network")
    
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()

drone = Drone("C:\\Users\\S B S\\Documents\\neural_drone\\neural_drone\\resources\\drone.png", pygame.math.Vector2(800, 500), screen)
propeller_path = "C:\\Users\\S B S\\Documents\\neural_drone\\neural_drone\\resources\\propeller.png"

p = Propeller(propeller_path, pygame.math.Vector2(100, 50))
import time
import matplotlib.pyplot as plt

t = time.time()
fl = False
fr = False
while True:
    p.draw()
    print(drone.fl)
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
                # drone.lastpos = pygame.math.Vector2(drone.pos.x, drone.pos.y)
                # left = False
                fl = False

            if event.key == pygame.K_e:
                # right = False
                fr = False
    # fr = random.random() > 0.5
    # fl = random.random() > 0.5
    if (fr == False):
        drone.fr *= 0.95
    else:
        drone.fr += 0.02
        drone.fr = min(drone.fr, 0.5)
    if (fl == False):
        drone.fl *= 0.95
    else:
        drone.fl += 0.02
        drone.fl = min(drone.fl, 0.5)
    drone.update()
    drone.draw()
    pygame.display.flip()     
    clock.tick(75)
    screen.fill(0)
    # print(time.time() - t)
    if (time.time() - t > 20):
        x = [x[0] for x in drone.l]
        y = [y[1] for y in drone.l]
        plt.plot(x, y)
        plt.show()
        break