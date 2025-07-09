from typing import List

class KnightPathStats:
    """
    Tracks and summarizes statistics for multiple knight pathfinding results.
    """

    def __init__(self):
        """
        Initialize an empty statistics tracker.
        """
        self.results: List[dict] = []


    def add_result(self, result: dict) -> None:
        """
        Add a single test result to the tracker.
        """
        self.results.append(result)


    def summary(self) -> dict:
        """
        Compute summary statistics over all results.

        Returns:
            dict: Aggregated metrics including test counts, timings, and speedups.
        """
        total_tests = len(self.results)
        failed_tests = sum(1 for r in self.results if r['failed'])
        total_fallbacks = sum(r['fallbacks'] for r in self.results)

        total_time_kq = sum(r['time_kq'] for r in self.results)
        total_time_bfs = sum(r['time_bfs'] for r in self.results)
        total_time_eval = sum(r['time_eval'] for r in self.results)

        kq_speedups = [r['kq_speedup'] for r in self.results if r['kq_speedup'] != float('inf')]
        eval_speedups = [r['eval_speedup'] for r in self.results if r['eval_speedup'] != float('inf')]

        avg_kq_time = total_time_kq / total_tests if total_tests else 0
        avg_bfs_time = total_time_bfs / total_tests if total_tests else 0
        avg_eval_time = total_time_eval / total_tests if total_tests else 0

        avg_kq_speedup = sum(kq_speedups) / len(kq_speedups) if kq_speedups else 0
        avg_eval_speedup = sum(eval_speedups) / len(eval_speedups) if eval_speedups else float('inf')

        return {
            "total_tests": total_tests,
            "failed_tests": failed_tests,
            "total_fallbacks": total_fallbacks,
            "avg_kq_time": avg_kq_time,
            "avg_bfs_time": avg_bfs_time,
            "avg_eval_time": avg_eval_time,
            "avg_kq_speedup": avg_kq_speedup,
            "avg_eval_speedup": avg_eval_speedup
        }