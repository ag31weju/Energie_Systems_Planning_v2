from enum import Enum


class BackdropFeature(Enum):
    GRASSLAND = "Grassland"
    MOUNTAIN = "Mountain"
    SEA = "Sea"
    RIVER = "River"
    BEACH = "Beach"


class Position:
    def __init__(self, x, y):
        if 0 <= x < 10 and 0 <= y < 10:
            self.x = x
            self.y = y
        else:
            raise ValueError(
                "Position must be within a 10x10 grid (0-9 for both x and y)."
            )

    def __repr__(self):
        return f"Position(x={self.x}, y={self.y})"

    def distance_to(self, other):
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5
