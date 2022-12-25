import pygame
import math

# local imports
from propeller import Propeller

WIDTH, HEIGHT = (1280, 720) # (1920, 1080)
class Drone:
    def __init__(self, pos, screen):
        self.size = pygame.math.Vector2(100, 50)
        self.image = pygame.transform.scale(pygame.image.load("C:\\Users\\S B S\\Documents\\neural_drone\\neural_drone\\resources\\drone.png"), self.size)
        self.rotated_image = pygame.transform.rotate(self.image, 0)
        self.pos = pygame.math.Vector2(pos.x, pos.y)
        self.rotated_image_rect = self.rotated_image.get_rect(center = self.pos)
        self.screen = screen
        self.left_prop = Propeller(self.screen, pygame.math.Vector2(100, 50), left= 1)
        self.right_prop = Propeller(self.screen, pygame.math.Vector2(100, 50), left= 0)
        self.friction = 0.05
        self.gravity = 0.5 # 0.5ze
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
        self.left_prop.draw()
        self.right_prop.draw()
        # self.left_prop.draw()
        # self.right_prop.draw()

    def update(self):
        self.updateForces()
    
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
        pass
    
    def updateFR(self):
        pass

    def updatePhi(self):
        self.phia = (self.getFL() - self.getFR()) * self.radius
        self.phiv = self.phiv * 0.975 + self.phia
        self.phi = self.phi + self.phiv
        pass
    
    def inScreen(self):
        w, h = pygame.display.get_surface().get_size()
        return (self.pos.x > 0 and self.pos.x < w and self.pos.y > 0 and self.pos.y < h)

        
def degToRad(deg):
    return deg * math.pi / 180

def radToDeg(rad):
    return rad * 180 / math.pi
