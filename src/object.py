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

    def draw(self):
        # self.screen.blit(self.rotated_image, self.rotated_image_rect)
        self.screen.blit(self.image, self.image.get_rect())
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

    def pushRight(self, angle):
        """rotate the object having the right end as the center"""
        self.rotate(angle,pygame.math.Vector2(0, 0))
        pass

    def rotate1(self, angle, pivot, offset):
        surface = self.screen
        rotated_image = pygame.transform.rotozoom(surface, -angle, 1)  # Rotate the image.
        rotated_offset = offset.rotate(angle)  # Rotate the offset vector.
        # Add the offset vector to the center/pivot point to shift the rect.
        rect = rotated_image.get_rect(center=pivot+rotated_offset)
        self.rotated_image = rotated_image
        self.rotated_image_rect = rect

    def pushLeft(self, angle):
        """rotate the object having the left end as the center"""
        # self.rotate1(angle, self.pos/2, pygame.math.Vector2(10,10))
        pygame.transform.rotate(self.image, angle)

        pass
