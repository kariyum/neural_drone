from copyreg import dispatch_table
import pygame
import math

class Object:
    def __init__(self, src, pos, screen):
        # src for image source
        self.mass = 1
        self.friction = 0.05
        self.oriPos = pygame.math.Vector2(pos.x, pos.y)
        self.pos = pygame.math.Vector2(pos.x, pos.y)
        self.size = pygame.math.Vector2(100, 50)
        self.acc = pygame.math.Vector2(0, 0)
        self.vel = pygame.math.Vector2(0, 0)
        self.angAcc = pygame.math.Vector2(0, 0)
        self.image = pygame.transform.scale(pygame.image.load(src), self.size)
        self.rotated_image = pygame.transform.rotate(self.image, 0)
        self.rotated_image_rect = self.rotated_image.get_rect(center = self.pos)
        self.screen = screen
        self.rightPivot = pygame.math.Vector2(self.pos.x + self.size.x/2 * math.cos(2*math.pi * (25)/360),
                                             self.pos.y - self.size.x/2 * math.sin(2*math.pi * (25)/360))
        
        self.leftPivot = pygame.math.Vector2(self.pos.x - self.size.x/2 * math.cos(-2*math.pi * (-25)/360),
                                             self.pos.y - self.size.x/2 * math.sin(-2*math.pi * (-25)/360))
        
        self.angularAccR = 0
        self.angularAccL = 0

        self.rotationAngleR = 0
        self.rotationAngleL = 0
        
        self.rotationSpeedR = 0
        self.rotationSpeedL = 0

    def draw(self):
        self.screen.blit(self.rotated_image, self.rotated_image_rect)
        # self.screen.blit(self.image, self.image.get_rect())
        # self.screen.blit(self.rotated_image, self.pos)

    def rotate(self, angle, pivot):
        pos = self.pos
        image = self.image
        originPos = pivot
        # offset from pivot to center
        image_rect = image.get_rect(topleft = (pos.x - originPos.x, pos.y-originPos.y))
        offset_center_to_pivot = pygame.math.Vector2(pos) - image_rect.center
        
        # roatated offset from pivot to center
        rotated_offset = offset_center_to_pivot.rotate(-angle)

        # roatetd image center
        rotated_image_center = (pos.x - rotated_offset.x, pos.y - rotated_offset.y)

        # get a rotated image
        self.rotated_image = pygame.transform.rotate(image, angle)
        self.rotated_image_rect = self.rotated_image.get_rect(center = rotated_image_center)
        
    
    def updatePosition(self):
        self.pos.x += self.vel.x
        self.pos.y += self.vel.y
    
    def updateAcceleration(self):
        self.acc.x = 0
        self.acc.y = 0

    def updateVelocity(self):
        self.vel.x = self.vel.x*(1-self.friction) + self.acc.x
        self.vel.y = self.vel.y*(1-self.friction) + self.acc.y

    def applyGravity(self):
        self.addForce(pygame.math.Vector2(0, 1))

    def updateAngularAcceleration(self):
        """Updates angular acceleration base on forces applied"""
        self.angAcc.x = 0
        self.angAcc.y = 0

    
    def applyForces(self):
        self.updateVelocity()
        self.updatePosition()

                
    def addForce(self, a):
        self.acc += a
    
    def update(self):
        self.applyGravity()
        self.applyForces()
        self.updateAcceleration()
        self.draw()

    def pushRight(self, angle = 0):
        """rotate the object having the right end as the center"""

        self.updateRotationAngle()

        angle = self.rotationAngleL + self.rotationAngleR


        self.rotate(angle, self.size/2)
        myangle = angle-25
        # self.leftPivot = pygame.math.Vector2(self.pos.x - self.size.x/2 * math.cos(-2*math.pi * (myangle)/360),
        #                                      self.pos.y - self.size.x/2 * math.sin(-2*math.pi * (myangle)/360))
        
        intialPos = pygame.math.Vector2(self.pos.x - self.size.x/2 * math.cos(-2*math.pi * -myangle/360), 
                                        self.pos.y - self.size.x/2 * math.sin(2*math.pi * -myangle/360))
        

        displacement = intialPos - self.leftPivot
        self.pos -= displacement
        pygame.draw.circle(self.screen, (255,255,255), intialPos, 10)
        pygame.draw.circle(self.screen, (255,255,0), self.leftPivot, 10)
        # pygame.draw.circle(self.screen, (255,0,255), self.rightPivot, 10)
        self.rightPivot = pygame.math.Vector2(self.pos.x + self.size.x/2 * math.cos(2*math.pi * (myangle+50)/360),
                                              self.pos.y - self.size.x/2 * math.sin(2*math.pi * (myangle+50)/360))

        # self.rotated_image = pygame.transform.rotate(self.image, angle)
        pass


    def pushLeft(self, angle = 0):
        """rotate the object having the left end as the center"""

        self.updateRotationAngle()
        angle = self.rotationAngleL + self.rotationAngleR


        self.rotate(angle, self.size/2)

        # myangle = angle+
        myangle = angle+25
        
        # self.rightPivot = pygame.math.Vector2(self.pos.x + self.size.x/2 * math.cos(2*math.pi * myangle/360),
        #                                      self.pos.y - self.size.x/2 * math.sin(2*math.pi * myangle/360))
        

        intialPos = pygame.math.Vector2(self.pos.x + self.size.x/2 * math.cos(2*math.pi * myangle/360), 
                                        self.pos.y - self.size.x/2 * math.sin(2*math.pi * myangle/360))
        

        displacement = pygame.math.Vector2(int(intialPos.x), int(intialPos.y)) - pygame.math.Vector2(int(self.rightPivot.x), int(self.rightPivot.y))
        
        self.pos = self.pos - displacement
        self.leftPivot = pygame.math.Vector2(self.pos.x - self.size.x/2 * math.cos(-2*math.pi * (myangle-50)/360),
                                             self.pos.y - self.size.x/2 * math.sin(-2*math.pi * (myangle-50)/360))


        pygame.draw.circle(self.screen, (255,255,255), intialPos, 10)
        pygame.draw.circle(self.screen, (255,100,255), self.rightPivot, 10)
        # pygame.draw.circle(self.screen, (0,200,200), self.leftPivot, 10)

        # self.rotated_image = pygame.transform.rotate(self.image, angle)
        pass
    
    def updateRotationAngle(self):
        pass
    def thrustRight(self):
        self.angularAccL = self.angularAccL - 0.1
        self.angularAccR = self.angularAccR + 0.03

    def thrustLeft(self):
        self.angularAccR = self.angularAccR + 0.1
        self.angularAccL = self.angularAccL - 0.03


    def decelerateR(self):
        self.angularAccR *=0.95
    
    def decelerateL(self):
        self.angularAccL *=0.95

    def updateRotationAngleR(self):
        self.rotationSpeedR = self.rotationSpeedR * 0.8 + self.angularAccR 
        self.rotationAngleR -= self.rotationSpeedR

    def updateRotationAngleL(self):
        self.rotationSpeedL = self.rotationSpeedL * 0.8 + self.angularAccL 
        self.rotationAngleL -= self.rotationSpeedL
    def update(self):
        self.updateRotationAngleR()
        self.pushLeft()
        self.updateRotationAngleL()
        self.pushRight()
        self.draw()