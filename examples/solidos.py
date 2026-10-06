# The five Platonic solids above a floor grid, drawn with the root Engine3D.
# Run it from the repository root with: python examples/solidos.py
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

import Engine3D
import pygame
import math
from Engine3D import Vector3, Matrix


def transformVectorYZ(vector, y, z):
    rotationY = Matrix([[math.cos(y), 0, -math.sin(y)],
                        [0          , 1           , 0],
                        [math.sin(y), 0,  math.cos(y)]])
    rotationZ = Matrix([[math.cos(z) , math.sin(z), 0],
                        [-math.sin(z), math.cos(z), 0],
                        [0           , 0          , 1]])
    return(rotationZ * rotationY * vector)


# The five Platonic solids, each scaled so that all its vertices lie on a sphere
# of radius 0.7. The edges are the pairs of vertices at the smallest distance.

phi = (1 + math.sqrt(5)) / 2


def cyclic(points):
    result = []
    for (a, b, c) in points:
        result += [(a, b, c), (b, c, a), (c, a, b)]
    return(result)


def signs(a, b, c):
    result = []
    for sa in ([1, -1] if a != 0 else [1]):
        for sb in ([1, -1] if b != 0 else [1]):
            for sc in ([1, -1] if c != 0 else [1]):
                result.append((sa * a, sb * b, sc * c))
    return(result)


tetrahedron = [(1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1)]
cube = signs(1, 1, 1)
octahedron = cyclic(signs(1, 0, 0))
icosahedron = cyclic(signs(0, 1, phi))
dodecahedron = signs(1, 1, 1) + cyclic(signs(0, 1 / phi, phi))


def makeSolid(points, center, radius):
    size = math.sqrt(points[0][0] ** 2 + points[0][1] ** 2 + points[0][2] ** 2)
    vertices = [center + Vector3(x, y, z) * (radius / size) for (x, y, z) in points]
    shortest = min((vertices[i] - vertices[j]).module for i in range(len(vertices)) for j in range(i))
    edges = []
    for i in range(len(vertices)):
        for j in range(i):
            if (vertices[i] - vertices[j]).module < shortest * 1.01:
                edges.append((vertices[i], vertices[j]))
    return(edges)


# The solids stand in a ring in front of the camera, above a square floor grid.
sceneCenter = Vector3(8, 0, -1)
floor = -1.2
edges = []
solids = [tetrahedron, cube, octahedron, dodecahedron, icosahedron]
for k in range(5):
    angle = 2 * math.pi * k / 5
    edges += makeSolid(solids[k], sceneCenter + Vector3(math.cos(angle), math.sin(angle), 0) * 1.9, 0.7)

for i in range(-3, 4):
    edges.append((sceneCenter + Vector3(i, -3, floor), sceneCenter + Vector3(i, 3, floor)))
    edges.append((sceneCenter + Vector3(-3, i, floor), sceneCenter + Vector3(3, i, floor)))


# Start above the ring, looking down at its centre, so that no two solids overlap on screen
Engine3D.CameraYRotation = 0.42
Engine3D.CameraZRotation = 0.3
Engine3D.cameraPosition = sceneCenter - transformVectorYZ(Vector3(1, 0, 0), Engine3D.CameraYRotation, Engine3D.CameraZRotation) * 7.5


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

    Engine3D.screen.fill(Engine3D.black)
    for (start, end) in edges:
        Engine3D.renderLine(start, end)

    pygame.display.flip()
