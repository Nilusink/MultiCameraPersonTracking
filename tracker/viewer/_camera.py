"""
_camera.py
27. October 2023

<description>

Author:
Nilusink
"""
from ursina import Entity, Vec3 as UVec3, rgb, destroy
import typing as tp

from ..camera import CameraConfig
from ..tools import Track, Vec3
from ._shapes import line


class Camera(Entity):
    distance: int = 10
    _last_track_entities: list[Entity]

    def __init__(self, config: CameraConfig) -> None:
        self._config = config
        self._last_track_entities = []

        p = config.position
        pos = UVec3(p.x, p.z, p.y)

        super().__init__(
            model='sphere',
            position=pos,
            color=rgb(255, 255, 255),
            scale=.1
        )

        # create "cone" in front of camera
        l1 = config.direction.copy()
        l1.angle_xy += config.fov.x / 2
        l1.angle_xz += config.fov.y / 2
        l1.length = self.distance
        l1 += config.position

        l2 = config.direction.copy()
        l2.angle_xy += config.fov.x / 2
        l2.angle_xz -= config.fov.y / 2
        l2.length = self.distance
        l2 += config.position

        l3 = config.direction.copy()
        l3.angle_xy -= config.fov.x / 2
        l3.angle_xz += config.fov.y / 2
        l3.length = self.distance
        l3 += config.position

        l4 = config.direction.copy()
        l4.angle_xy -= config.fov.x / 2
        l4.angle_xz -= config.fov.y / 2
        l4.length = self.distance
        l4 += config.position

        # forward lines
        line(config.position, l1)
        line(config.position, l2)
        line(config.position, l3)
        line(config.position, l4)

        # closing lines
        line(l1, l2, l4, l3, close=True)

    @property
    def config(self) -> CameraConfig:
        return self._config

    def update_tracks(self, tracks: tp.Iterable[Track]) -> None:
        # delete old entities
        for e in self._last_track_entities:
            destroy(e)

        # assign to temporary variables for better readability
        px, py = self.config.resolution.xy
        fx, fy = self.config.fov.xy

        for track in tracks:
            x, y = track.last_box.center.xy

            # cast to 3d direction
            angle_xy = -((x - px / 2) / px) * fx
            angle_xz = -((y - py / 2) / py) * fy

            trace = Vec3.from_polar(angle_xy, angle_xz, 1)
            trace.angle_xz += self.config.direction.angle_xz
            trace.angle_xy += self.config.direction.angle_xy
            trace.length = self.distance * 2

            self._last_track_entities.append(
                line(self.config.position, self.config.position + trace, color=rgb(255, 0, 0))
            )

