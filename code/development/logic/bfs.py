
from collections import deque
from model.point import Point

class KnightBFS:
    """
    Performs a brute-force Breadth-First Search (BFS) to find the shortest path 
    for a knight from a start position to an end position on an infinite board.

    Attributes:
        KNIGHT_MOVES(arr[Point]): List of all moves knight can make
    """
    KNIGHT_MOVES = [
        Point(-2, -1), Point(-1, -2), Point(1, -2), Point(2, -1),
        Point(2, 1), Point(1, 2), Point(-1, 2), Point(-2, 1)
    ]


    def __init__(self, A: 'Point', B: 'Point') -> None:
        """
        Initialize the KnightBFS with a starting point A and target point B.

        Args:
            A (Point): The starting position of the knight.
            B (Point): The target position to reach.
        """
        self.A = A
        self.B = B


    def fpath(self) -> list:
        """
        Execute BFS to find the shortest path from start to end.

        Returns:
            Optional[List[Point]]: The shortest path as a list of Points.
        """
        if self.A == self.B:
            return [self.A]

        visited = set()
        queue = deque([(self.A, [self.A])])

        while queue:
            current_pos, path = queue.popleft()

            if current_pos == self.B:
                return path

            for move in self.KNIGHT_MOVES:
                next_pos = current_pos + move
                if next_pos not in visited:
                    visited.add(next_pos)
                    queue.append((next_pos, path + [next_pos]))

        return [] 

