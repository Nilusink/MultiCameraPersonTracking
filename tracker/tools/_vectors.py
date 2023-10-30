"""
_vectors.py
27. October 2023

defines 2d and 3d vectors

Author:
Nilusink
"""
from copy import deepcopy, copy
import typing as tp
import math as m


class Vec2:
    """
    Simple 2D vector class
    """
    x: float
    y: float
    angle: float
    length: float

    # creation of new elements
    def __init__(self) -> None:
        self.__x: float = 0
        self.__y: float = 0
        self.__angle: float = 0
        self.__length: float = 0

    @classmethod
    def from_cartesian(cls, x: float, y: float) -> tp.Self:
        p = cls()
        p.x = x
        p.y = y

        return p

    @classmethod
    def from_polar(cls, angle: float, length: float) -> tp.Self:
        p = cls()
        while angle > 2 * m.pi:
            angle -= 2 * m.pi
        while angle < 0:
            angle += 2 * m.pi
        p.angle = angle
        p.length = length

        return p

    # variable getters / setters
    @property
    def x(self) -> float:
        return self.__x

    @x.setter
    def x(self, value: float) -> None:
        self.__x = value
        self.__update("c")

    @property
    def y(self) -> float:
        return self.__y

    @y.setter
    def y(self, value: float) -> None:
        self.__y = value
        self.__update("c")

    @property
    def xy(self) -> tuple[float, float]:
        return self.x, self.y

    @property
    def angle(self) -> float:
        """
        value in radian
        """
        return self.__angle

    @angle.setter
    def angle(self, value: float) -> None:
        """
        value in radian
        """
        self.__angle = value
        self.__update("p")

    @property
    def length(self) -> float:
        return self.__length

    @length.setter
    def length(self, value: float) -> None:
        self.__length = value
        self.__update("p")

    @property
    def polar(self) -> tuple[float, float]:
        """
        :return: angle, length
        """
        return self.angle, self.length

    # maths
    def __add__(self, other) -> tp.Self:
        if isinstance(other, self.__class__):
            return self.__class__.from_cartesian(
                x=self.x + other.x,
                y=self.y + other.y
            )

        return self.__class__.from_cartesian(
            x=self.x + other,
            y=self.y + other
        )

    def __sub__(self, other) -> tp.Self:
        if isinstance(other, self.__class__):
            return self.__class__.from_cartesian(
                x=self.x - other.x,
                y=self.y - other.y
            )

        return self.__class__.from_cartesian(x=self.x - other, y=self.y - other)

    def __mul__(self, other) -> tp.Self:
        if isinstance(other, self.__class__):
            return self.__class__.from_polar(
                angle=self.angle + other.angle,
                length=self.length * other.length
            )

        return self.__class__.from_cartesian(x=self.x * other, y=self.y * other)

    def __truediv__(self, other) -> tp.Self:
        return self.__class__.from_cartesian(x=self.x / other, y=self.y / other)

    # internal functions
    def __update(self, calc_from: str) -> None:
        """
        :param calc_from: polar (p) | cartesian (c)
        """
        if calc_from in ("p", "polar"):
            self.__x = m.cos(self.angle) * self.length
            self.__y = m.sin(self.angle) * self.length
            return

        elif calc_from in ("c", "cartesian"):
            self.__length = m.sqrt(self.x**2 + self.y**2)
            self.__angle = m.atan2(self.y, self.x)
            return

        raise ValueError("Invalid value for \"calc_from\"")

    def __abs__(self) -> float:
        return m.sqrt(self.x**2 + self.y**2)

    def __repr__(self) -> str:
        return f"<\n" \
               f"\tVector:\n" \
               f"\tx:{self.x}\ty:{self.y}\n" \
               f"\tangle:{self.angle}\tlength:{self.length}\n" \
               f">"

    def copy(self, use_deepcopy: bool = False) -> tp.Self:
        new = self.__class__()
        if use_deepcopy:
            new.__dict__ = deepcopy(self.__dict__)
        else:
            new.__dict__ = copy(self.__dict__)

        return new

    # static methods.
    # creation of new instances
    @staticmethod
    def from_dict(dictionary: dict) -> "Vec2":
        if "x" in dictionary and "y" in dictionary:
            return Vec2.from_cartesian(x=dictionary["x"], y=dictionary["y"])

        elif "angle" in dictionary and "length" in dictionary:
            return Vec2.from_polar(angle=dictionary["angle"], length=dictionary["length"])

        else:
            raise KeyError("either (x & y) or (angle & length) must be in dict!")

    @staticmethod
    def normalize_angle(value: float) -> float:
        while value > 2 * m.pi:
            value -= 2 * m.pi

        while value < -2 * m.pi:
            value += 2 * m.pi
        return value


class Vec3:
    """
    Simple 3D vector class
    """
    x: float
    y: float
    z: float
    angle_xy: float
    angle_xz: float
    length_xy: float
    length: float

    def __init__(self):
        self.__x: float = 0
        self.__y: float = 0
        self.__z: float = 0
        self.__angle_xy: float = 0
        self.__angle_xz: float = 0
        self.__length_xy: float = 0
        self.__length: float = 0

    @property
    def x(self) -> float:
        return self.__x

    @x.setter
    def x(self, value: float) -> None:
        self.__x = value
        self.__update("c")

    @property
    def y(self) -> float:
        return self.__y

    @y.setter
    def y(self, value: float) -> None:
        self.__y = value
        self.__update("c")

    @property
    def z(self) -> float:
        return self.__z

    @z.setter
    def z(self, value: float) -> None:
        self.__z = value
        self.__update("c")

    @property
    def xyz(self) -> tp.Tuple[float, float, float]:
        """
        :return: x, y, z
        """
        return self.x, self.y, self.z

    @xyz.setter
    def xyz(self, value: tp.Tuple[float, float, float]) -> None:
        """
        :param value: (x, y, z)
        """
        self.__x, self.__y, self.__z = value
        self.__update("c")

    @property
    def angle_xy(self) -> float:
        return self.__angle_xy

    @angle_xy.setter
    def angle_xy(self, value: float) -> None:
        self.__angle_xy = self.normalize_angle(value)
        self.__update("p")

    @property
    def angle_xz(self) -> float:
        return self.__angle_xz

    @angle_xz.setter
    def angle_xz(self, value: float) -> None:
        self.__angle_xz = self.normalize_angle(value)
        self.__update("p")

    @property
    def length_xy(self) -> float:
        """
        can't be set
        """
        return self.__length_xy

    @property
    def length(self) -> float:
        return self.__length

    @length.setter
    def length(self, value: float) -> None:
        self.__length = value
        self.__update("p")

    @property
    def polar(self) -> tp.Tuple[float, float, float]:
        """
        :return: angle_xy, angle_xz, length
        """
        return self.angle_xy, self.angle_xz, self.length

    @polar.setter
    def polar(self, value: tp.Tuple[float, float, float]) -> None:
        """
        :param value: (angle_xy, angle_xz, length)
        """
        self.__angle_xy = self.normalize_angle(value[0])
        self.__angle_xz = self.normalize_angle(value[1])
        self.__length = value[2]
        self.__update("p")

    @classmethod
    def from_polar(
            cls,
            angle_xy: float,
            angle_xz: float,
            length: float
    ) -> tp.Self:
        """
        create a Vector3D from polar form
        """
        v = cls()
        v.polar = angle_xy, angle_xz, length
        return v

    @classmethod
    def from_cartesian(cls, x: float, y: float, z: float) -> tp.Self:
        """
        create a Vector3D from cartesian form
        """
        v = cls()
        v.xyz = x, y, z
        return v

    @staticmethod
    def calculate_with_angles(
            length: float,
            angle1: float,
            angle2: float
    ) -> tp.Tuple[float, float, float]:
        """
        calculate the x, y and z components of length facing (angle1, angle2)
        """
        tmp = m.cos(angle2) * length
        z = m.sin(angle2) * length
        x = m.cos(angle1) * tmp
        y = m.sin(angle1) * tmp

        return x, y, z

    @staticmethod
    def normalize_angle(angle: float) -> float:
        """
        removes "overflow" from an angle
        """
        while angle > 2 * m.pi:
            angle -= 2 * m.pi

        while angle < 0:
            angle += 2 * m.pi

        return angle

    # maths
    def __neg__(self) -> tp.Self:
        self.xyz = [-el for el in self.xyz]
        return self

    def __add__(self, other) -> tp.Self:
        if isinstance(other, self.__class__):
            return self.__class__.from_cartesian(
                x=self.x + other.x,
                y=self.y + other.y,
                z=self.z + other.z
            )

        return self.__class__.from_cartesian(
            x=self.x + other,
            y=self.y + other,
            z=self.z + other
        )

    def __sub__(self, other) -> tp.Self:
        if isinstance(other, self.__class__):
            return self.__class__.from_cartesian(
                x=self.x - other.x,
                y=self.y - other.y,
                z=self.z - other.z
            )

        return self.__class__.from_cartesian(
            x=self.x - other,
            y=self.y - other,
            z=self.z - other
        )

    def __mul__(self, other) -> tp.Self:
        if isinstance(other, self.__class__):
            return self.__class__.from_polar(
                angle_xy=self.angle_xy + other.angle_xy,
                angle_xz=self.angle_xz + other.angle_xz,
                length=self.length * other.length
            )

        return self.__class__.from_cartesian(
            x=self.x * other,
            y=self.y * other,
            z=self.z * other
        )

    def __truediv__(self, other) -> tp.Self:
        return self.__class__.from_cartesian(
            x=self.x / other,
            y=self.y / other,
            z=self.z / other
        )

    def copy(self, use_deepcopy: bool = False) -> tp.Self:
        new = self.__class__()
        if use_deepcopy:
            new.__dict__ = deepcopy(self.__dict__)
        else:
            new.__dict__ = copy(self.__dict__)

        return new

    def normalize(self) -> tp.Self:
        """
        cut the vectors length to 1
        """
        new = self.copy(use_deepcopy=True)
        new.length = 1
        return new

    # internal functions
    def __update(self, calc_from: str) -> None:
        match calc_from:
            case "p":
                self.__length_xy = m.cos(self.angle_xz) * self.length
                x, y, z = self.calculate_with_angles(
                    self.length,
                    self.angle_xy,
                    self.angle_xz
                )
                self.__x = x
                self.__y = y
                self.__z = z

            case "c":
                self.__length_xy = m.sqrt(self.y**2 + self.x**2)
                self.__angle_xy = m.atan2(self.y, self.x)
                self.__angle_xz = m.atan2(self.z, self.__length_xy)
                self.__length = m.sqrt(self.x**2 + self.y**2 + self.z**2)

    def __repr__(self) -> str:
        return f"<\n" \
               f"\tVector3D:\n" \
               f"\tx:{self.x}\ty:{self.y}\tz:{self.z}\n" \
               f"\tangle_xy:{self.angle_xy}\tangle_xz:{self.__angle_xz}" \
               f"\tlength:{self.length}\n" \
               f">"


# tests
if __name__ == "__main__":
    v1 = Vec3.from_cartesian(-.2, 1, 0)
    v2 = Vec3.from_cartesian(.2, 1, 0)
    print(v1, v2, Vec3.from_cartesian(0, 1, 0))
