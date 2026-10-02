import Engine3D
import pygame


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


Engine3D.init()


running = True
while running == True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    Engine3D.fillScreen((0, 0, 0))
    Engine3D.renderCube(Vector3(10, 0, 0), 2)
    pygame.draw.circle(Engine3D.screen, (255, 255, 255), [400, 400], 5)
    Engine3D.flipScreen()
    pygame.display.flip()