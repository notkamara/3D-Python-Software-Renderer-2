import pygame, math, transform
from pygame.locals import *

width = 1600
height = 900


hWidth = width/2
hHeight = height/2

gameExit = False

fov = 90

pygame.init()
screen = pygame.display.set_mode((width,height))
pygame.display.set_caption("3D Triangles!")

##CUBE COORDINATES:
##(FRONT 4)
##(10,10,10)
##(10,-10,10)
##(-10,-10,10)
##(-10,10,10)
##(BACK 4)
##(10,10,-10)
##(10,-10,-10)
##(-10,-10,-10)
##(-10,10,-10)
mesh = [[(-100,0,100),(100,0,100),(100,0,-100),(-100,0,-100)],[(1,1,1),(1,-1,1),(-1,-1,1),(-1,1,1)],[(1,1,-1),(1,-1,-1),(-1,-1,-1),(-1,1,-1)],[(-1,1,-1),(-1,1,1),(-1,-1,1),(-1,-1,-1)],[(1,1,1),(1,1,-1),(1,-1,-1),(1,-1,1)],[(1,1,1),(1,1,-1),(-1,1,-1),(-1,1,1)],[(-1,-1,-1),(-1,-1,1),(1,1,-1),(1,-1,-1)]]
meshColours = [(0,0,255),(0,0,255),(0,255,0),(255,0,255),(0,255,55),(255,255,0),(255,255,255)]

global pointsNotInView

pointsNotInView = 0

cameraPos = (0,0,0)

cameraX = 0
cameraY = 0
cameraZ = 0

cameraVX = 0
cameraVY = 0
cameraVZ = 0

camRotX = 0
camRotY = 0

fps = 30
clock = pygame.time.Clock()

mouseVector = (0,0)

pygame.mouse.set_visible(False)
pygame.event.set_grab(1)

def render(pos1, pos2, pos3, pos4, colour):    
    if not pointsNotInView == 4:
        pygame.draw.polygon(screen, colour, [pos1, pos2, pos3, pos4,], 0)

def screenSpaceTransform(point):
    global pointsNotInView
    tempX, tempY, tempZ = transform.rotateX((transform.rotateY(transform.translate(point, cameraPos), -camRotY, (0,0,0))), camRotX, (0,0,0))
    if tempZ < 0:
        pointsNotInView += 1
    return (((tempX/math.fabs(tempZ) * math.tan((fov * math.pi)/360)) * hWidth) + hWidth, ((-tempY/math.fabs(tempZ) * math.tan((fov * math.pi)/360)) * hWidth) + hHeight)  

while not gameExit:
    clock = pygame.time.Clock()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameExit = True
        if event.type == KEYDOWN:
            if event.key == K_w:
                cameraVZ = 0.5000000000000000000000000001
            elif event.key == K_s:
                cameraVZ = -0.5000000000000000000000000001
            elif event.key == K_a:
                cameraVX = -0.5000000000000000000000000001
            elif event.key == K_d:
                cameraVX = 0.5000000000000000000000000001
            elif event.key == K_SPACE:
                cameraVY = 0.5
            elif event.key == K_c:
                cameraVY = -0.5000000000000000000000000001
            elif event.key == K_ESCAPE:
                gameExit = True
        if event.type == KEYUP:
            if event.key == K_w:
                cameraVX = 0
                cameraVZ = 0
            elif event.key == K_s:
                cameraVX = 0                
                cameraVZ = 0
            elif event.key == K_a:
                cameraVX = 0
            elif event.key == K_d:
                cameraVX = 0
            elif event.key == K_SPACE:
                cameraVY = 0
            elif event.key == K_c:
                cameraVY = 0

    mouseVector = pygame.mouse.get_rel()
    mouseVX, mouseVY = mouseVector

    camRotX -= mouseVY
    camRotY += mouseVX

    if camRotX < -90:
        camRotX = -90
    elif camRotX > 90:
        camRotX = 90

    if camRotY <= -180:
        camRotY += 360
    elif camRotY > 180:
        camRotY -= 360
    
    cameraX += cameraVZ * math.sin(math.radians(camRotY)) + cameraVX * math.cos(math.radians(camRotY))
    cameraY += cameraVY
    cameraZ += cameraVZ * math.cos(math.radians(camRotY)) - cameraVX * math.sin(math.radians(camRotY))
    
    cameraPos = (-cameraX, -cameraY, -cameraZ)

    screen.fill((0,0,0))
    for faces in range(0,6):
        pointsNotInView = 0
        pos1_2D = screenSpaceTransform(mesh[faces][0])
        pos2_2D = screenSpaceTransform(mesh[faces][1])
        pos3_2D = screenSpaceTransform(mesh[faces][2])
        pos4_2D = screenSpaceTransform(mesh[faces][3])
        render(pos1_2D, pos2_2D, pos3_2D, pos4_2D, meshColours[faces])
    pygame.display.update()
    clock.tick(fps)
pygame.quit()
quit()
