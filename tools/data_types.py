"""
data_types.py
25. October 2023

<description>

Author:
Nilusink
"""
from dataclasses import dataclass
import typing as tp
import math


@dataclass()
class Vec2:
    x: int | float
    y: int | float

    @property
    def length(self) -> float:
        return math.sqrt((self.x**2) + (self.y**2))

    @property
    def xy(self) -> tuple[int | float, int | float]:
        return self.x, self.y

    def __add__(self, other: tp.Self | tp.Sequence[list | float]) -> tp.Self:
        if isinstance(other, self.__class__):
            return Vec2(self.x + other.x, self.y + other.y)

        return Vec2(self.x + other[0], self.y + other[1])

    def __sub__(self, other: tp.Self | tp.Sequence[list | float]) -> tp.Self:
        if isinstance(other, self.__class__):
            return Vec2(self.x - other.x, self.y - other.y)

        return Vec2(self.x - other[0], self.y - other[1])

    def __abs__(self) -> tp.Self:
        return Vec2(abs(self.x), abs(self.y))

    def __repr__(self) -> str:
        return f"Point<{self.x}, {self.y}>"


@dataclass()
class Box:
    position: Vec2
    size: Vec2

    @property
    def center(self) -> Vec2:
        return Vec2(
            self.position.x + self.size.x / 2,
            self.position.y + self.size.y / 2
        )

    def __repr__(self) -> str:
        return f"Box<position: {self.position}, size: {self.size}>"


if __name__ == "__main__":
    b = Box(Vec2(1, 2), Vec2(2, 3))
    print(b, b.center)
