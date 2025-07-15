
import math
from dataclasses import dataclass
from model.point import Point

@dataclass
class Sequence:
    """
    Abstract representation of knight move counts as a sequence indices (n, m).

    This class translates 2D knight board coordinates into sequence indices that
    help evaluate the minimum number of moves required to reach a target square.

    Attributes:
        n (int): The primary sequence index related to diagonal positioning.
        m (int): The secondary index describing vertical offset from the diagonal.

    Note:
        For the full mathematical derivation of the sequence formulas, 
        see the KnightQuest.pdf.
    """
    n: int
    m: int


    @classmethod
    def from_point(cls, r: 'Point') -> 'Sequence':
        """
        Convert a 2D board coordinate (Point) to a sequence index (n, m).

        The transformation maps the canonical knight position in the first Quadrant 
        on the grid to the sequence indices that parameterize the minimum move counts.

        Args:
            r (Point): The coordinate point on the board.

        Returns:
            Sequence: The corresponding sequence indices (n, m).
        """
        # Reference point to sequence indices logic.
        if r.x == 2 and r.y == 2:
            # Special case 
            return cls(5, 0)
        elif r.y <= (r.x / 2):
            n = r.x
            m = math.ceil(n / 2) - r.y
        else:
            delta = math.ceil((2 * r.y - r.x) / 3)
            rr_x = r.x + delta
            rr_y = r.y - delta
            n = rr_x
            m = math.ceil(n / 2) - rr_y

        return cls(n, m)


    def diagonal(self) -> int:
        """
        Computes the sequence value for a knight moving repeatedly along the base vector (2, 1), 
        which corresponds to movement along the y = x/2 diagonal.

        The knight's movement space exhibits symmetry across several diagonals: y = x/2, y = 2x,
        y = -2x, and y = -x/2. Due to this symmetry, the minimum number of moves required
        to reach a point between the lines y and y = x is the same as that required to
        reach a point between y = x and x. This diagonal evaluation captures the minimal path 
        length in such symmetric regions.

        Returns:
            int: The sequence value (minimum moves) along the y = x/2 diagonal.
        """      
        return (self.n + 3 * (self.n % 2)) // 2


    def vertical(self) -> int:
        """
        Calculate the vertical offset value below the diagonal sequence value. This offset
        represents the vertical offset relative to the diagonal sequence value.

        Returns:
            int: The vertical offset value.
        """
        return ((self.n - 1) % 2) * (self.m % 2) - (self.n % 2) * (self.m % 2)


    def value(self) -> int:
        """
        Compute the complete sequence value representing minimum number of moves needed to
        reach a square. Combines diagonal and vertical components to yield the minimum move 
        count needed to reach a target square on the board in the canonical region (Quadrant I).

        Returns:
            int: The estimated minimum number of moves to reach the position.
        """      
        if self.n == 1 and self.m == 1:
            return 3

        return self.diagonal() + self.vertical()
    
        