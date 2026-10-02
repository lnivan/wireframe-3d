import Engine3D
import pygame
import math
import time
import random

e = 0.000001



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




def is_between(n1, n2, n3):
    if (n1 < n3 and n3 < n2) or (n2 < n3 and n3 < n1):
        return(True) 
    


def penepromax(m1, m2, m3):
    if is_between(m1.x, m2.x, m3.x) and is_between(m1.y, m2.y, m3.y) and is_between(m1.z, m2.z, m3.z):
        return(True)





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



speed = 10



points = []

for i in range(100):
    points.append(Vector3(random.random() - 0.5, random.random() - 0.5, random.random() - 0.5) * 20)







rx = Matrix([[1, 0, 0],
             [0, 0.7071, -0.7071],
             [0, 0.7071, 0.7071]])


ry = Matrix([[0.7071, 0, 0.7071],
             [0, 1, 0],
             [-0.7071, 0, 0.7071]])


rz = Matrix([[0.7071, -0.7071, 0],
             [0.7071, 0.7071, 0],
             [0, 0, 1]])





testicularTorsion = []

for p in points:
    testicularTorsion.append(ry*(rx*(rz*p)))


print(testicularTorsion)


maxx = 0
minx = 0
maxy = 0
miny = 0
maxz = 0
minz = 0



for testiculo in range(len(testicularTorsion)):

    if testicularTorsion[testiculo].x > testicularTorsion[maxx].x:
        maxx = testiculo

    if testicularTorsion[testiculo].x < testicularTorsion[minx].x:
        minx = testiculo


    if testicularTorsion[testiculo].y > testicularTorsion[maxy].y:
        maxy = testiculo

    if testicularTorsion[testiculo].y < testicularTorsion[miny].y:
        miny = testiculo


    if testicularTorsion[testiculo].z > testicularTorsion[maxz].z:
        maxz = testiculo

    if testicularTorsion[testiculo].z < testicularTorsion[minx].z:
        minz = testiculo


print(maxx, minx, maxy, miny, maxz, minz)


pointscolor = []
for pene in points:
    if    penepromax(points[maxx], points[maxy], pene) or    penepromax(points[maxx], points[miny], pene) or    penepromax(points[maxx], points[maxz], pene) or     penepromax(points[maxx], points[minz], pene) or    penepromax(points[minx], points[maxy], pene) or    penepromax(points[minx], points[miny], pene) or      penepromax(points[minx], points[maxz], pene) or   penepromax(points[minx], points[minz], pene) or  penepromax(points[maxz], points[maxy], pene) or    penepromax(points[maxz], points[miny], pene) or    penepromax(points[minz], points[maxy], pene) or      penepromax(points[minz], points[miny], pene):
        pointscolor.append(red)
    else:
        pointscolor.append(white)

def dibujarcubo(p1, p2):
    Engine3D.renderLine(Vector3(p1.x, p1.y, p1.z), Vector3(p1.x, p2.y, p1.z), (200, 200, 200))
    Engine3D.renderLine(Vector3(p1.x, p2.y, p1.z), Vector3(p2.x, p2.y, p1.z), (200, 200, 200))
    Engine3D.renderLine(Vector3(p2.x, p2.y, p1.z), Vector3(p2.x, p1.y, p1.z), (200, 200, 200))
    Engine3D.renderLine(Vector3(p2.x, p1.y, p1.z), Vector3(p1.x, p1.y, p1.z), (200, 200, 200))

    Engine3D.renderLine(Vector3(p1.x, p1.y, p2.z), Vector3(p1.x, p2.y, p2.z), (200, 200, 200))
    Engine3D.renderLine(Vector3(p1.x, p2.y, p2.z), Vector3(p2.x, p2.y, p2.z), (200, 200, 200))
    Engine3D.renderLine(Vector3(p2.x, p2.y, p2.z), Vector3(p2.x, p1.y, p2.z), (200, 200, 200))
    Engine3D.renderLine(Vector3(p2.x, p1.y, p2.z), Vector3(p1.x, p1.y, p2.z), (200, 200, 200))

    Engine3D.renderLine(Vector3(p1.x, p1.y, p1.z), Vector3(p1.x, p1.y, p2.z), (200, 200, 200))
    Engine3D.renderLine(Vector3(p2.x, p1.y, p1.z), Vector3(p2.x, p1.y, p2.z), (200, 200, 200))
    Engine3D.renderLine(Vector3(p1.x, p2.y, p1.z), Vector3(p1.x, p2.y, p2.z), (200, 200, 200))
    Engine3D.renderLine(Vector3(p2.x, p2.y, p1.z), Vector3(p2.x, p2.y, p2.z), (200, 200, 200))




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
                yVel = speed
            if event.key == pygame.K_a:
                yVel = -speed
            if event.key == pygame.K_w:
                xVel = speed
            if event.key == pygame.K_s:
                xVel = -speed
            if event.key == pygame.K_LCTRL:
                zVel = speed
            if event.key == pygame.K_LSHIFT:
                zVel = -speed
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
    '''
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
    '''


    Engine3D.renderLine(Vector3(e, e, e), Vector3(0.854,0.500,-0.146) * 10, white)
    Engine3D.renderLine(Vector3(e, e, e), Vector3(-0.146,0.500,0.854) * 10, white)
    Engine3D.renderLine(Vector3(e, e, e), Vector3(0.500,-0.707,0.500) * 10, white)

    Engine3D.renderLine(Vector3(e, e, e), Vector3(0.854,0.500,-0.146) * (-10), white)
    Engine3D.renderLine(Vector3(e, e, e), Vector3(-0.146,0.500,0.854) * (-10), white)
    Engine3D.renderLine(Vector3(e, e, e), Vector3(0.500,-0.707,0.500) * (-10), white)


    Engine3D.renderLine(Vector3(e, e, e), Vector3(10, e, e), red)
    Engine3D.renderLine(Vector3(e, e, e), Vector3(e, 10, e), red)
    Engine3D.renderLine(Vector3(e, e, e), Vector3(e, e, 10), red)
    
    Engine3D.renderLine(Vector3(e, e, e), Vector3(-10, e, e), red)
    Engine3D.renderLine(Vector3(e, e, e), Vector3(e, -10, e), red)
    Engine3D.renderLine(Vector3(e, e, e), Vector3(e, e, -10), red)


    dibujarcubo(points[maxx], points[maxy])
    dibujarcubo(points[maxx], points[miny])

    dibujarcubo(points[maxx], points[maxz])
    dibujarcubo(points[maxx], points[minz])

    
    dibujarcubo(points[minx], points[maxy])
    dibujarcubo(points[minx], points[miny])

    dibujarcubo(points[minx], points[maxz])
    dibujarcubo(points[minx], points[minz])

    
    dibujarcubo(points[maxz], points[maxy])
    dibujarcubo(points[maxz], points[miny])

    dibujarcubo(points[minz], points[maxy])
    dibujarcubo(points[minz], points[miny])


    for p in range(len(points)):
        Engine3D.renderPoint(points[p], pointscolor[p])
    

    pygame.display.flip()