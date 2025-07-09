
from dataclasses import dataclass

@dataclass(frozen=True)
class Point:
    """
    Immutable 2D point representing coordinates on a Cartesian plane.

    Attributes:
        x (int): The x-coordinate.
        y (int): The y-coordinate.

    This class supports vector addition using the + operator,
    allowing easy computation of relative positions.

    Includes a static method to create a Point from a complex number,
    rounding the real and imaginary parts to the nearest integers.
    """
    x: int
    y: int


    def __add__(self, second_point: 'Point') -> 'Point':
        """
        Add two points coordinate-wise.

        Args:
            second_point (Point): The second point to add.

        Returns:
            Point: A new Point representing the sum of coordinates.
        """
        return Point(self.x + second_point.x, self.y + second_point.y)


    def __sub__(self, other: 'Point') -> 'Point':
        """
        Subtract two points coordinate-wise.

        Args:
            other (Point): The other point to subtract.

        Returns:
            Point: A new Point representing the difference of coordinates.
        """
        return Point(self.x - other.x, self.y - other.y)


    @staticmethod
    def from_complex(z: complex) -> 'Point':
        """
        Create a Point from a complex number by rounding its real and imaginary parts.

        Args:
            z (complex): The complex number to convert.

        Returns:
            Point: A new Point with integer coordinates derived from z.
        """
        return Point(round(z.real), round(z.imag))