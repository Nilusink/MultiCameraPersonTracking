from tracker.camera import CameraConfig
from tracker.tools import Vec2, Vec3
from tracker.viewer import Viewer
from tracker.tools import Track, Box


CAMERAS = [
    CameraConfig(
        Vec3.from_cartesian(-1, 0, 2.3),
        Vec3.from_cartesian(.2, 1, -.3),
        Vec2.from_cartesian(.88888888, .5),
        Vec2.from_cartesian(1920, 1080)
    ),
    CameraConfig(
        Vec3.from_cartesian(1, 0, 2.3),
        Vec3.from_cartesian(-.2, 1, -.3),
        Vec2.from_cartesian(.88888888, .5),
        Vec2.from_cartesian(1920, 1080)
    )
]


t = Track(Box(Vec2.from_cartesian(10, 10), Vec2.from_cartesian(10, 10)))
t2 = Track(Box(Vec2.from_cartesian(960, 540), Vec2.from_cartesian(960, 540)))


v = Viewer(cameras=CAMERAS)

while True:
    v.ursina.step()
    v.update_tracks(((t2,), (t,)))

