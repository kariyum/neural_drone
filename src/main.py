from pygame import Vector2
from object import *

def blitRotate(surf, image, pos, originPos, angle):
    # offset from pivot to center
    image_rect = image.get_rect(topleft = (pos[0] - originPos[0], pos[1]-originPos[1]))
    offset_center_to_pivot = pygame.math.Vector2(pos) - image_rect.center
    # roatated offset from pivot to center
    rotated_offset = offset_center_to_pivot.rotate(-angle)
    # roatetd image center
    rotated_image_center = (pos[0] - rotated_offset.x, pos[1] - rotated_offset.y)
    # get a rotated image
    rotated_image = pygame.transform.rotate(image, angle)
    rotated_image_rect = rotated_image.get_rect(center = rotated_image_center)
    # rotate and blit the image
    surf.blit(rotated_image, rotated_image_rect)



def main():
    # initialize the pygame module
    pygame.init()
    # load and set the logo
    pygame.display.set_caption("Genetic Neural Network")
     
    screen = pygame.display.set_mode((1280, 720))
    clock = pygame.time.Clock()

    image = pygame.transform.scale(pygame.image.load("./resources/drone.png"), (100, 50))
    
    rotationAngle = 1
    pos = pygame.math.Vector2(350, 350)
    vy = 0
    
    
    drone = Object("./resources/drone.png", pygame.math.Vector2(300, 350), screen)
    left = False
    right = False
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                raise SystemExit
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_z:
                    left = True
                if event.key == pygame.K_e:
                    right = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_z:
                    drone.lastpos = pygame.math.Vector2(drone.pos.x, drone.pos.y)
                    left = False
                if event.key == pygame.K_e:
                    right = False
            

        if (right):
            drone.thrustRight()
        else:
            drone.decelerateR()
        if (left):
            drone.thrustLeft()
        else:
            drone.decelerateL()
        # rotatedImage = pygame.transform.rotate(image, rotationAngle)
        # screen.blit(rotatedImage, (posx, posy))
        
        vy = 2
        pos.y += 0.05
        # blitRotate(screen, image, (pos.x, pos.y), (100/2, 50/2), rotationAngle)

        # drone.update()
        # drone.rotate(rotationAngle, pygame.math.Vector2(drone.size.x, 0))

               
        
        drone.update()
        drone.leftPivot -= pygame.math.Vector2(0,-vy)
        drone.rightPivot -= pygame.math.Vector2(0,-vy)
        # stop here 
        pygame.display.flip()     
        clock.tick(60)
        screen.fill(0)

if __name__=="__main__":
    main()