
import time
from model.point import Point
from logic.kq import KnightQuest
from logic.bfs import KnightBFS

class KnightPathCase:
    """
    Represents and evaluates a single knight pathfinding test case. Encapsulates all logic to:
      - Run a knight pathfinding test from a given start to target position.
      - Compare the KnightQuest algorithm against a baseline BFS implementation.
      - Validate correctness of both paths (ensuring legal knight moves).
      - Measure and return timing metrics for full path generation and evaluation.
      - Compute relative speedups of KnightQuest and its evaluation logic.
      - Check for fallbacks or failure conditions in KnightQuest.

    The test case is considered successful if:
      - Both KnightQuest and BFS produce valid paths.
      - The paths are of equal length (even if not identical).
    
    Attributes:
        A (Point): Starting coordinate of the knight.
        B (Point): Target coordinate the knight should reach.
    """

    def __init__(self, A: Point, B: Point):
        """
        Initializes a KnightPathCase with start and target positions.

        Args:
            A (Point): Starting position of the knight.
            B (Point): Target position to reach.
        """
        self.A = A
        self.B = B


    @staticmethod
    def is_valid_knight_path(path: list[Point], A: Point, B: Point) -> bool:
        """
        Validates that a given path:
            - Begins at the correct start point.
            - Ends at the correct target point.
            - Consists only of valid knight moves.

        Args:
            path (list[Point]): The sequence of points in the path.
            A (Point): The expected starting point.
            B (Point): The expected ending point.

        Returns:
            bool: True if the path is valid, False otherwise.
        """
        if not path or path[0] != A or path[-1] != B:
            return False
        
        for a, b in zip(path, path[1:]):
            dx, dy = abs(a.x - b.x), abs(a.y - b.y)

            if sorted((dx, dy)) != [1, 2]:
                return False
            
        return True


    def run(self) -> dict:
        """
        Executes the test case using both the KnightQuest and BFS solvers.

        Performs the following:
            - Computes a full path using KnightQuest.
            - Estimates the number of moves using KnightQuest's fast evaluator.
            - Computes a full path using BFS.
            - Measures computation time for all methods.
            - Validates both paths (start, end, and legal knight steps).
            - Compares path lengths and structure.
            - Calculates speedup of KnightQuest vs BFS, and evaluator vs BFS.
            - Tracks fallback use and flags any failed conditions.

        Returns:
            dict: A dictionary containing relevant information
        """

        kq = KnightQuest(self.A, self.B)
        bfs = KnightBFS(self.A, self.B)

        # KnightQuest path generation timing.
        t0 = time.perf_counter()
        path_kq = kq.fpath()
        t1 = time.perf_counter()
        time_kq = t1 - t0

        # KnightQuest evaluation timing.
        t0 = time.perf_counter()
        kq_eval = kq.feval(self.A, self.B)
        t1 = time.perf_counter()
        time_eval = t1 - t0

        # BFS path generation timing.
        t0 = time.perf_counter()
        path_bfs = bfs.fpath()
        t1 = time.perf_counter()
        time_bfs = t1 - t0

        # KnightQuest and BFS path validation.
        valid_kq = self.is_valid_knight_path(path_kq, self.A, self.B)
        valid_bfs = self.is_valid_knight_path(path_bfs, self.A, self.B)

        # KnightQuest evaluation function validation
        eval_matches = kq_eval == len(path_bfs) - 1

        # KnightQuest and BFS path length comparison.
        same_length = len(path_kq) == len(path_bfs)
        same_path = path_kq == path_bfs

        # Speed ratios (handle zero division)
        kq_speedup = float('inf') if time_kq == 0 else time_bfs / time_kq
        eval_speedup = float('inf') if time_eval == 0 else time_bfs / time_eval

        failed = not (valid_kq and valid_bfs and same_length and eval_matches)

        return {
            "start": self.A,
            "target": self.B,
            "path_kq": path_kq,
            "kq_eval": kq_eval,
            "path_bfs": path_bfs,
            "valid_kq": valid_kq,
            "valid_bfs": valid_bfs,
            "eval_matches": eval_matches,
            "same_length": same_length,
            "same_path": same_path,
            "time_kq": time_kq,
            "time_bfs": time_bfs,
            "time_eval": time_eval,
            "kq_speedup": kq_speedup,
            "eval_speedup": eval_speedup,
            "fallbacks": kq.fallback_count,
            "failed": failed
        }