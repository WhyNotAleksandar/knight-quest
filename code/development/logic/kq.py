
from model.point import Point
from model.sequence import Sequence

class KnightQuest:
    """
    Evaluates the minimum number of moves for a knight to reach a target square on a board
    and reconstructs a path by rotating base knight move vectors in the complex plane.

    The knight's base move vectors (1, 2) and (2, 1) are rotated according to the quadrant 
    of the current position relative to the start, and the algorithm chooses the best move 
    based on an evaluation function that estimates the remaining minimum moves.
    """

    def __init__(self, A: 'Point', B: 'Point') -> None:
        """
        Initialize the KnightQuest with a starting point A and target point B.

        Args:
            A (Point): The starting position of the knight.
            B (Point): The target position to reach.
        """
        self.A = A
        self.B = B

        self._p = [B]
        self._u = complex(1, 2)
        self._v = complex(2, 1)
        self.fallback_count = 0


    def _fseg(self, k: 'Point') -> None:
        """
        Append a new path segment (Point) to the path.

        Args:
            k (Point): The next point to add to the path.
        """
        self._p.append( self._p[-1] + k)


    def _fquad(self, d: 'Point') -> int:
        """
        Determine the rotation index (0 to 3) based on the quadrant of vector d.
        This index represents multiples of 90-degree counterclockwise rotations 
        used to orient knight move vectors.

        Args:
            d (Point): The vector to determine quadrant for.

        Returns:
            int: Rotation index (0 to 3).
        """
        theta = 0

        if d.x >= 0 and d.y >= 0:
            theta = 0
        elif d.x >= 0 and d.y < 0:
            theta = 3
        elif d.x < 0 and d.y >= 0:
            theta = 1
        elif d.x < 0 and d.y < 0:
            theta = 2

        # Adjacent square adjustment.
        if abs(d.x) == 1 and abs(d.y) == 1:
            theta += 1

        return theta


    def _frot(self, z: complex, theta: int) -> 'Point':
        """
        Rotate a complex number z by 90 degrees multiplied by theta and convert to a Point.

        Args:
            z (complex): The complex vector to rotate.
            theta (int): The number of 90-degree rotations (counterclockwise).

        Returns:
            Point: The rotated point.
        """        
        return Point.from_complex(z * (1j) ** theta)


    def _fref(self, d: 'Point') -> 'Point':
        """
        Reflect a point d to the canonical region between axes x and y = x/2. Exploits 
        symmetry of the knight's moves so that points like (-3, 5) and (5, 3) are 
        considered equivalent.

        Args:
            d (Point): The point to reflect.

        Returns:
            Point: The reflected point in the canonical region.
        """
        return Point(max(abs(d.x), abs(d.y)), min(abs(d.x), abs(d.y)))


    def feval(self, A: 'Point', B: 'Point') -> int:
        """
        Evaluate the minimum number of knight moves needed to reach the point B
        from the start point A.

        Args:
            A (Point): The starting position of the knight.
            B (Point): The target position to reach.

        Returns:
            int: The minimum number of moves remaining.
        """
        d = A - B
        r = self._fref(d)
        return Sequence.from_point(r).value()


    def fmove(self) -> None:
        """
        Determine and perform the next knight move towards the start point A. Moves are 
        chosen by rotating base knight vectors (1,2) and (2,1) according to the quadrant 
        of the current distance vector and evaluating which candidate move reduces the 
        minimum moves remaining.
        """
        d = self.A - self._p[-1]
        r = self._fref(d)
        s = Sequence.from_point(r)

        # Evaluate the outcome of applying each possible move direction:
        # - Rotate the base move vectors (_u and _v) according to the direction
        # - Apply them to the current path endpoint to get two candidate positions
        # - Measure the distance vector from the goal (A) for each
        # - Reflect those distances to the first quadrant
        # - Convert the resulting vectors into Sequence objects for evaluation
        candidate_u = self._frot(self._u, self._fquad(d))
        candidate_v = self._frot(self._v, self._fquad(d))
        path_u = self._p[-1] + candidate_u
        path_v = self._p[-1] + candidate_v
        du = self.A - path_u
        dv = self.A - path_v
        ru = self._fref(du)
        rv = self._fref(dv)
        su = Sequence.from_point(ru)
        sv = Sequence.from_point(rv)

        if min(d.x, d.y) != 0 and abs(max(d.x, d.y) / min(d.x, d.y)) == 2:
            # If (d) is an integer multiple of a base knight move, decompose 
            # it into unit knight steps and append each to the path.
            count = max(abs(d.x), abs(d.y)) // 2
            unit_x = d.x // count
            unit_y = d.y // count
            unit_move = Point(unit_x, unit_y)

            for _ in range(count):
                self._fseg(unit_move)

        # Check if the move decreases the evaluation by exactly 1 (i.e., one step closer).
        # If so, commit the corresponding candidate vector to the current path.
        elif s.value() - su.value() == 1:
            self._fseg(candidate_u)
        elif s.value() - sv.value() == 1:
            self._fseg(candidate_v)

        # To prevent stalling or incorrect behavior, a heuristic (e.g., choosing the move 
        # whose vector aligns better with the distance vector) is applied here.       
        else:
            dot_u = candidate_u.x * d.x + candidate_u.y * d.y
            dot_v = candidate_v.x * d.x + candidate_v.y * d.y

            if dot_u >= dot_v:
                self._fseg(candidate_u)
            else:
                self._fseg(candidate_v)

            # Track how many times fallback logic was triggered (for debugging/analysis)
            self.fallback_count += 1


    def fpath(self) -> list:
        """
        Construct the full knight path from the target back to the start point. Repeatedly 
        applies moves using fmove until the evaluation function returns zero, meaning the 
        knight has reached the start point.

        Returns:
            list: The list of path segment (Points) in correct order.
        """
        while self.feval(self.A, self._p[-1]) > 0:
            self.fmove()

        return self._p[::-1]