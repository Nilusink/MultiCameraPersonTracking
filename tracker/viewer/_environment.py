"""
_environment.py
27. October 2023

<description>

Author:
Nilusink
"""
from ursina import Ursina, EditorCamera, rgb, window, Entity
import typing as tp

from ..tools import Track
from ..tools import Vec3
from ..camera import CameraConfig
from ._camera import Camera
from ._shapes import line


class Viewer:
    _cameras: list[Camera]

    def __init__(
            self,
            cameras: tp.Iterable[CameraConfig],
    ) -> None:
        self._cameras = []
        self.ursina = Ursina()
        window.color = (0, 0, 0, 0)

        # floor
        Entity(
            model='plane',
            scale=50,
            color=rgb(50, 50, 50)
        )

        # cameras
        for cam in cameras:
            self._cameras.append(Camera(cam))

        line(Vec3(), Vec3.from_cartesian(1, 0, 0), color=rgb(255, 0, 0))
        line(Vec3(), Vec3.from_cartesian(0, 1, 0), color=rgb(0, 255, 0))
        line(Vec3(), Vec3.from_cartesian(0, 0, 1), color=rgb(0, 0, 255))

        EditorCamera()  # add camera controls for orbiting and moving the camera

    def update_tracks(self, tracks: tuple[tp.Iterable[Track], ...]) -> None:
        """
        :param tracks: structure: ([tracks per camera], [tracks per other camera])
        """
        for i, cam_tracks in enumerate(tracks):
            self._cameras[i].update_tracks(cam_tracks)
