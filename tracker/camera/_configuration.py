"""
_configuration.py
25. October 2023

Defines a camera and its properties

Author:
Nilusink
"""
from dataclasses import dataclass
from ..tools import Vec2, Vec3


@dataclass(frozen=True)
class CameraConfig:
    position: Vec3
    direction: Vec3
    fov: Vec2  # in rad
    resolution: Vec2

