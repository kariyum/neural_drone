import pygame
import math
import random
import cv2
import numpy as np
import time
import matplotlib.pyplot as plt

WIDTH, HEIGHT = (1280, 720)
def c2ImageToSurface(cvImage):
    if cvImage.dtype.name == 'uint16':
        cvImage = (cvImage / 256).astype('uint8')
    size = cvImage.shape[1::-1]
    if len(cvImage.shape) == 2:
        cvImage = np.repeat(cvImage.reshape(size[1], size[0], 1), 3, axis = 2)
        format = 'RGB'
    else:
        format = 'RGBA' if cvImage.shape[2] == 4 else 'RGB'
        cvImage[:, :, [0, 2]] = cvImage[:, :, [2, 0]]
    surface = pygame.image.frombuffer(cvImage.flatten(), size, format)
    return surface.convert_alpha() if format == 'RGBA' else surface.convert()

class Propeller:
    def __init__(self, src, pos):
        self.dy = 0
        self.pos = pos
        self.phi2 = 0
        self.phi = 0
        self.rayon = 55
        self.size = pygame.math.Vector2(30, 10)
        # self.image = pygame.transform.scale(pygame.image.load(src), self.size)
        self.image = cv2.imread(r"resources/step1.png", cv2.IMREAD_UNCHANGED)
        self.screen = screen
        # self.rotated_image = pygame.transform.rotate(self.image, 0)
        # self.rotated_image_rect = self.rotated_image.get_rect(center = self.pos)
        # animation needs
        self.animation_step = 0
        self.images = ["resources/step"+str(i)+".png" for i in range(1,5)]
        self.rx = np.array([[1,0,0,0],
                        [0,1,0,0],
                        [0,0,1,0],
                        [0,0,0,1]],np.float32)  
        self.ry = np.array([[1,0,0,0],
                        [0,1,0,0],
                        [0,0,1,0],
                        [0,0,0,1]],np.float32)
        self.rz = np.array([[1,0,0,0],
                        [0,1,0,0],
                        [0,0,1,0],
                        [0,0,0,1]],np.float32)  
        self.trans = np.array([[1,0,0,0],
                        [0,1,0,0],
                        [0,0,1,200],   #400 to move the image in z axis 
                        [0,0,0,1]],np.float32)
        self.proj2dto3d = np.array([[1,0,-self.image.shape[1]/2],
                      [0,1,-self.image.shape[0]/2],
                      [0,0,0],
                      [0,0,1]],np.float32)
        self.proj3dto2d = np.array([ [200,0,self.image.shape[1]/2,0],
                                [0,200,self.image.shape[0]/2,0],
                                [0,0,1,0] ],np.float32)
        self.x = 0.0 
        self.y = 0.0
        self.z = 0.0 

    def draw(self):
        # self.rotated_image = pygame.transform.flip(self.rotated_image, True, False)
        # self.screen.blit(self.rotated_image, self.rotated_image_rect)
        # image = pygame.transform.scale(pygame.image.load(self.images[self.animation_step]), self.size)
        self.rotate()
        #create a surface with the size as the array
        # surf = pygame.Surface((self.rotated_image.shape[0], self.rotated_image.shape[1]))
        # draw the array onto the surface

        # self.rotated_image = pygame.image.load(r"resources/rotated_image.png")
        # self.screen.blit(self.rotated_image, self.pos)
        
        
        # pygame.surfarray.blit_array(surf, self.rotated_image)
        # transform the surface to screen size
        # print(self.rotated_image[:,:,:2])
        # self.screen.blit(pygame.surfarray.make_surface(self.rotated_image[:,:,1:4]), self.pos)
        surf = c2ImageToSurface(self.rotated_image)
        surf = pygame.transform.scale(surf, self.size)
        rotated_image = pygame.transform.rotate(surf, self.phi)
        rotated_image_rect = rotated_image.get_rect(center = self.pos)
        self.screen.blit(rotated_image, rotated_image_rect)
    def rotate(self):
        # scale_percent = 200 
        # width = int(self.image.shape[1] * scale_percent / 100)
        # height = int(self.image.shape[0] * scale_percent / 100)
        # dim = (width, height)
        # self.image = cv2.resize(self.image, (150, 50), interpolation = cv2.INTER_LINEAR)

        ax = float(self.x * (math.pi / 180.0)) #0
        ay = float(self.y * (math.pi / 180.0)) 
        az = float(self.z * (math.pi / 180.0)) #0
        
        self.rx[1,1] = math.cos(ax) #0
        self.rx[1,2] = -math.sin(ax) #0
        self.rx[2,1] = math.sin(ax) #0
        self.rx[2,2] = math.cos(ax) #0
        
        self.ry[0,0] = math.cos(ay)
        self.ry[0,2] = -math.sin(ay)
        self.ry[2,0] = math.sin(ay)
        self.ry[2,2] = math.cos(ay)
        
        self.rz[0,0] = math.cos(az) #0
        self.rz[0,1] = -math.sin(az) #0
        self.rz[1,0] = math.sin(az) #0
        self.rz[1,1] = math.cos(az) #0
        
        r = self.rx.dot(self.ry).dot(self.rz) # if we remove the lines we put    r=ry
        final = self.proj3dto2d.dot(self.trans.dot(r.dot(self.proj2dto3d)))
        
        
        dst = cv2.warpPerspective(self.image, final, (self.image.shape[1],self.image.shape[0]),None,cv2.INTER_LINEAR
                                ,cv2.BORDER_CONSTANT,(255,255,255))
        # print(final.shape, self.image.shape)
        # dst = np.dot(final, self.image) 
        # pygame.surfarray.blit_array(self.screen, dst[:,:,:3])
        # pygame.pixelcopy.array_to_surface(self.screen, dst[:,:,:3])
        # cv2.imshow("dst",dst)
        # cv2.imwrite("rotated_image"+str(i)+".jpg", dst)
        self.y = self.y + self.dy  # increase self.y angel by 3
        # self.x = self.x + 1
        # self.z += 1
        self.rotated_image = dst
        # cv2.imwrite(r"resources/rotated_image.png", dst)    

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

if __name__ == '__main__':
    pygame.init()
    # load and set the logo
    pygame.display.set_caption("Genetic Neural Network")
        
    screen = pygame.display.set_mode((1280, 720))
    clock = pygame.time.Clock()

    drone = Drone("C:\\Users\\S B S\\Documents\\neural_drone\\neural_drone\\resources\\drone.png", pygame.math.Vector2(800, 500), screen)
    propeller_path = "C:\\Users\\S B S\\Documents\\neural_drone\\neural_drone\\resources\\propeller.png"

    propeller1 = Propeller(propeller_path, pygame.math.Vector2(100, 50))
    propeller2 = Propeller(propeller_path, pygame.math.Vector2(100, 50))

    t = time.time()
    fl = False
    fr = False
    while True:
        t = time.time()
        # print(drone.fl)
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
        propeller1.dy = propeller1.dy * 0.4 + 50 * drone.getFL()
        propeller1.phi2 = -120 -30 + drone.phi
        propeller1.pos = drone.pos + (propeller1.rayon * math.cos(degToRad(propeller1.phi2)), propeller1.rayon * math.sin(degToRad(propeller1.phi2)))
        
        propeller2.dy = propeller2.dy * 0.4 + 50 * drone.getFR()
        propeller2.phi2 = -30 + drone.phi
        propeller2.pos = drone.pos + (propeller2.rayon * math.cos(degToRad(propeller2.phi2)), propeller2.rayon * math.sin(degToRad(propeller2.phi2)))
        
        propeller1.phi = -drone.phi
        propeller2.phi = -drone.phi
        drone.draw()
        propeller1.draw()
        propeller2.draw()
        pygame.display.flip()     
        clock.tick(75)
        screen.fill(0)
        # print(time.time() - t)
        print(1/(time.time() - t))
        if (time.time() - t > 20):
            x = [x[0] for x in drone.l]
            y = [y[1] for y in drone.l]
            plt.plot(x, y)
            plt.show()
            break