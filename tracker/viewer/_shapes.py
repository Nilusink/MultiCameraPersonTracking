"""
File:
shapes.py

used to create simple meshes with ursina

Author:
Nilusink
"""
from ursina import Entity, Mesh, Vec3 as UVec3
from ..tools import Vec3, Vec2


def line(*points: Vec3, close: bool = False, **kwargs) -> Entity:
    points = [UVec3(p.x, p.z, p.y) for p in points]

    if close:
        points.append(points[0])

    return Entity(model=Mesh(vertices=points, mode='line'), **kwargs)
