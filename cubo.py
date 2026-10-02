import Engine3D
import pygame
import math
import time





class Vector3:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.module = math.sqrt(x**2 + y**2 + z**2)

    def __add__(self, other):
        return(Vector3(self.x + other.x, self.y + other.y, self.z + other.z))

    def __sub__(self, other):
        return(Vector3(self.x - other.x, self.y - other.y, self.z - other.z))

    def __mul__(self, other):
        return(Vector3(self.x * other, self.y * other, self.z * other))
    
    def __truediv__(self, other):
        return(Vector3(self.x / other, self.y / other, self.z / other))

    def __pow__(self, other):
        return(self.x * other.x + self.y * other.y + self.z * other.z)

    def normalize(self):
        return(Vector3(self.x / self.module, self.y / self.module, self.z / self.module))






class VectorN:
    def __init__(self, coordinates):
        self.coordinates = coordinates
        self.module = 0
        for i in coordinates:
            self.module = self.module + i ** 2
        self.module = math.sqrt(self.module)
        self.size = len(coordinates)

    def __pow__(self, other):
        result = 0
        for i in range(self.size):
            result = result + self.coordinates[i] * other.coordinates[i]
        return(result)




class Matrix:
    def __init__(self, matrix):
        self.matrix = matrix
        self.size = (len(matrix), len(matrix[0]))

    def __mul__(self, other):
        otherIsVector = False
        if type(other) == Vector3:
            other = Matrix([[other.x, other.y, other.z]])
            otherIsVector = True
        result = []
        for x in range(other.size[0]):
            result.append([])
            for y in range(self.size[1]):
                row = []
                column = []
                for i in range(self.size[0]):
                    row.append(self.matrix[i][y])
                    column.append(other.matrix[x][i])
                result[x].append(VectorN(row) ** VectorN(column))
        if otherIsVector == True:
            return(Vector3(result[0][0], result[0][1], result[0][2]))
        else:
            return(Matrix(result))


def transformVectorYZ(vector, y, z):
    rotationY = Matrix([[math.cos(y), 0, -math.sin(y)],
                        [0          , 1           , 0],
                        [math.sin(y), 0,  math.cos(y)]])
    rotationZ = Matrix([[math.cos(z) , math.sin(z), 0],
                        [-math.sin(z), math.cos(z), 0],
                        [0           , 0          , 1]])
    return(rotationZ * rotationY * vector)


gameLength = 1400
gameWidth = 800

FOV = 100 * math.pi * 2 / 360
a = gameLength / (2 * math.sin(FOV / 2))
FocalLength = math.cos(FOV / 2) * a

cameraPosition = Vector3(0, 0, 0)
CameraZRotation = 0
CameraYRotation = 0

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)

deltaTime = 0
lastFrameTime = time.time()

pygame.init()
screen = pygame.display.set_mode((gameLength, gameWidth))

xVel = 0
yVel = 0
zVel = 0
rotating = False


running = True
while running == True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        mdX, mdY = pygame.mouse.get_rel()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 3:    
                rotating = True
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 3:    
                rotating = False
        if rotating:
            Engine3D.CameraYRotation = Engine3D.CameraYRotation + mdY * 0.001
            Engine3D.CameraZRotation = Engine3D.CameraZRotation - mdX * 0.001
        #if event.type == pygame.MOUSEBUTTONDOWN: 
         #   if event.button == 2:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                yVel = 1
            if event.key == pygame.K_a:
                yVel = -1
            if event.key == pygame.K_w:
                xVel = 1
            if event.key == pygame.K_s:
                xVel = -1
            if event.key == pygame.K_LCTRL:
                zVel = 1
            if event.key == pygame.K_LSHIFT:
                zVel = -1
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_ESCAPE: 
                running = False          
            if event.key == pygame.K_w or event.key == pygame.K_s:
                xVel = 0
            if event.key == pygame.K_a or event.key == pygame.K_d:
                yVel = 0
            if event.key == pygame.K_LCTRL or event.key == pygame.K_LSHIFT:
                zVel = 0

    Engine3D.cameraPosition = Engine3D.cameraPosition + (transformVectorYZ(Vector3(1, 0, 0), Engine3D.CameraYRotation, Engine3D.CameraZRotation) * xVel - transformVectorYZ(Vector3(0, 1, 0), Engine3D.CameraYRotation, Engine3D.CameraZRotation) * yVel - Vector3(0, 0, 1) * zVel) * 0.01

    deltaTime = time.time() - lastFrameTime
    lastFrameTime = time.time()

    screen.fill(black)
    Engine3D.renderLine(Vector3(10, 0, 0), Vector3(12, 0, 0))
    Engine3D.renderLine(Vector3(10, 0, 0), Vector3(10, 2, 0))
    Engine3D.renderLine(Vector3(10, 0, 0), Vector3(10, 0, 2))
    Engine3D.renderLine(Vector3(12, 2, 0), Vector3(12, 2, 2))
    Engine3D.renderLine(Vector3(12, 2, 0), Vector3(12, 0, 0))
    Engine3D.renderLine(Vector3(12, 2, 0), Vector3(10, 2, 0))
    Engine3D.renderLine(Vector3(12, 0, 0), Vector3(12, 0, 2))
    Engine3D.renderLine(Vector3(10, 2, 0), Vector3(10, 2, 2))
    Engine3D.renderLine(Vector3(10, 0, 2), Vector3(12, 0, 2))
    Engine3D.renderLine(Vector3(12, 0, 2), Vector3(12, 2, 2))
    Engine3D.renderLine(Vector3(12, 2, 2), Vector3(10, 2, 2))
    Engine3D.renderLine(Vector3(10, 2, 2), Vector3(10, 0, 2))

    pygame.display.flip()