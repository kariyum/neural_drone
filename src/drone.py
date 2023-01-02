import pygame
import math
import random

# local imports
from propeller import Propeller
from network import Network

WIDTH, HEIGHT = (1280, 720) # (1920, 1080)
class Drone:
    def __init__(self, screen, pos= pygame.math.Vector2(WIDTH/2, HEIGHT/2)):
        self.screen = screen
        self.size = pygame.math.Vector2(100, 50)
        self.image = pygame.transform.scale(pygame.image.load("C:\\Users\\S B S\\Documents\\neural_drone\\neural_drone\\resources\\drone.png"), self.size)
        self.left_prop = Propeller(self.screen, pygame.math.Vector2(100, 50), left= 1)
        self.right_prop = Propeller(self.screen, pygame.math.Vector2(100, 50), left= 0)
        self.rotated_image = pygame.transform.rotate(self.image, 0)
        self.init_pos = pos
        self.pos = pos.copy()
        self.rotated_image_rect = self.rotated_image.get_rect(center = self.pos)
        self.friction = 0.05
        self.gravity = 0.5 # 0.5ze
        self.radius = 1/2
        self.mass = 1
        self.init_dynamic_attributes()
    
    def revive(self):
        self.init_dynamic_attributes()
    
    def init_dynamic_attributes(self):
        self.pos = self.init_pos.copy()
        self.phiv = 0
        self.phia = 0
        self.phi = 0
        self.ax = 0
        self.ay = 0
        self.vx = 0
        self.vy = 0
        self.fl = 0
        self.fr = 0
    
    def draw(self, prop_anim):
        self.screen.blit(self.rotated_image, self.rotated_image_rect)
        self.left_prop.draw(prop_anim)
        self.right_prop.draw(prop_anim)
        # self.left_prop.draw()
        # self.right_prop.draw()

    def update(self, network, deltaTime):
        self.deltaTime = deltaTime
        actions= network.forward([[self.pos.x / WIDTH, self.pos.y / HEIGHT, self.fl*2, self.fr*2, self.ax, self.ay, self.vx, self.vy, self.phi / 360, self.phiv, self.phia]]) # multiplied by 2 for the range to be between 0 and 1
        self.left_acceleration, self.right_acceleration = [True if random.random() <= a else False for a in actions[-1]]
        self.updateForces()
        if (not self.inScreen()): return 1
        return 0
    
    def updateForces(self):
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
        self.updatePropellers()
    
    def updatePropellers(self):
        self.left_prop.update(power_rate= self.getFL(), drone_phi= self.phi, drone_position= self.pos)
        self.right_prop.update(power_rate= self.getFR(), drone_phi= self.phi, drone_position= self.pos)
    
    def getPhi(self):
        return degToRad(self.phi)
    
    def getFL(self):
        # return random.random()
        return self.fl

    def getFR(self):
        # return random.random()
        return self.fr

    def updateFL(self):
        if (self.left_acceleration):
            self.fl = min(self.fl + 0.02, 0.5)
        else:
            self.fl *= 0.95
    
    def updateFR(self):
        if (self.right_acceleration):
            self.fr = min(self.fr+0.02, 0.5)
        else:
            self.fr *= 0.95

    def updatePhi(self):
        self.phia = (self.getFL() - self.getFR()) * self.radius
        self.phiv = self.phiv * 0.975 + self.phia
        self.phi = self.phi + self.phiv
        pass
    
    def inScreen(self):
        w, h = pygame.display.get_surface().get_size()
        return (self.pos.x + 70> 0 and self.pos.x - 70 < w and self.pos.y + 70 > 0 and self.pos.y - 70 < h)

        
def degToRad(deg):
    return deg * math.pi / 180

def radToDeg(rad):
    return rad * 180 / math.pi
