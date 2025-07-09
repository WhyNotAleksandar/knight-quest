
import random
from typing import Optional
from model.point import Point
from tests.case import KnightPathCase
from tests.statistics import KnightPathStats
from tests.reporter import KnightPathReporter

class KnightPathTester:
    """
    Runs a batch of knight pathfinding test cases and reports results. 
    Supports console output or file logging.
    """
    def __init__(self, num_cases: int, max_coord: int, seed: Optional[int] = None):
        """
        Initialize with a list of (start, target) point pairs.
        """
        self._num_cases = num_cases
        self._max_coord = max_coord
        self._seed = seed

        self.cases = self._generate_random_cases()
        self.stats = KnightPathStats()
        self.reporter = KnightPathReporter()


    def _generate_random_cases(self) -> list[tuple[Point, Point]]:
        """
        Generate a list of random (start, target) Point pairs for knight path tests.

        Coordinates are chosen from -max_coord to +max_coord to test negative positions.
        Optionally accepts a seed for reproducibility.

        Args:
            num_cases (int): Number of test cases to generate.
            max_coord (int): Maximum absolute value for x and y coordinates (default 300).
            seed (Optional[int]): Seed value for reproducibility (default None).

        Returns:
            list[tuple[Point, Point]]: List of (start, target) point tuples.
        """
        if self._seed is not None:
            random.seed(self._seed)

        cases = []
        for _ in range(self._num_cases):
            start = Point(
                random.randint(-self._max_coord, self._max_coord),
                random.randint(-self._max_coord, self._max_coord)
            )
            target = Point(
                random.randint(-self._max_coord, self._max_coord),
                random.randint(-self._max_coord, self._max_coord)
            )
            cases.append((start, target))
        return cases


    def run_all_console(self) -> None:
        """
        Run all test cases and print formatted results to the console.
        """
        for start, target in self.cases:
            case = KnightPathCase(start, target)
            result = case.run()
            self.stats.add_result(result)
            print(self.reporter.format_case_result(result))

        summary = self.stats.summary()
        summary['max_coord'] = self._max_coord
        summary['seed'] = self._seed

        print(self.reporter.format_summary(summary))


    def run_all_file(self, filepath: str = "tests/output/log.txt") -> None:
        """
        Run all test cases and write formatted results to a file.

        Args:
            filepath (str): Destination path for output log file.
            Defaults to 'tests\\output\\log.txt'.
        """
        results = []

        for case_number, (start, target) in enumerate(self.cases, start=1):
            case = KnightPathCase(start, target)
            result = case.run()
            self.stats.add_result(result)
            results.append(result)

            print(f"Case {case_number} from {start} to {target} written to file.")

        summary = self.stats.summary()
        summary['max_coord'] = self._max_coord
        summary['seed'] = self._seed
        self.reporter.write_to_file(results, summary, filepath)

        print(f"All test cases written to {filepath}.")