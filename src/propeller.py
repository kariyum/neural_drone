# this class is for controlling / drawing the propeller
import pygame
import cv2
import numpy as np
import math

class Propeller:
    def __init__(self, screen, pos, left):
        self.phi_diff = -150 if left else -30
        self.dy = 0
        self.pos = pos
        self.phi2 = 0
        self.phi = 0
        self.rayon = 55
        self.size = pygame.math.Vector2(30, 10)
        # self.image = pygame.transform.scale(pygame.image.load(src), self.size)
        self.image = cv2.imread(r"resources/propeller.png", cv2.IMREAD_UNCHANGED)
        self.screen = screen
        # self.rotated_image = pygame.transform.rotate(self.image, 0)
        # self.rotated_image_rect = self.rotated_image.get_rect(center = self.pos)
        # animation needs
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
    
    def update(self, power_rate, drone_phi, drone_position):
        self.dy = self.dy * 0.4 + 50 * power_rate
        phi = self.phi_diff + drone_phi
        self.pos = drone_position + (self.rayon * math.cos(degToRad(phi)), self.rayon * math.sin(degToRad(phi)))
        self.phi = -drone_phi

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

def degToRad(deg):
    return deg * math.pi / 180

def radToDeg(rad):
    return rad * 180 / math.pi