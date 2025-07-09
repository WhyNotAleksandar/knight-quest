
from io import StringIO

class KnightPathReporter:
    """
    This class is responsible for generating representations of individual test case results, 
    summarizing aggregate statistics from multiple test cases and writing formatted results 
    and summary to a file.
    """
    def format_case_result(self, result: dict) -> str:
        """
        Format the output for a single test case.

        Includes:
          - Start and target points.
          - KnightQuest and BFS validity, path lengths, and timings.
          - Whether the paths have the same length or are identical.
          - Fallback usage in KnightQuest.
          - Speedup ratios between KnightQuest and BFS, and between feval and BFS.  
        
        Args:
            result (dict): A dictionary containing the result of a single test case,
            as returned by KnightPathCase.run().          

        Returns:
            str: Formatted string representation of the result.
        """
        out = StringIO()

        print(f"\nTesting from {result['start']} to {result['target']}", file=out)
        print(f"🎯 Minimum number of moves (feval): {result['kq_eval']}, Matches: {result['eval_matches']}", file=out)
        print(f"✅ KQ valid: {result['valid_kq']}, length: {len(result['path_kq'])}, time: {result['time_kq']:.6f}s", file=out)
        print(f"✅ BF valid: {result['valid_bfs']}, length: {len(result['path_bfs'])}, time: {result['time_bfs']:.6f}s", file=out)
        print(f"🔁 Same length: {result['same_length']}, Same path: {result['same_path']}", file=out)
        print(f"🧮 Fallbacks used: {result['fallbacks']}", file=out)

        if result['kq_speedup'] == float('inf'):
            print("⚠️ KQ ran too fast to measure speedup reliably.", file=out)
        elif result['kq_speedup'] > 1:
            print(f"🚀 KQ is {result['kq_speedup']:.2f}x faster than BFS", file=out)
        else:
            print(f"🐢 BFS is {1 / result['kq_speedup']:.2f}x faster than KQ", file=out)

        if result['eval_speedup'] == float('inf'):
            print("⚠️ feval too fast to measure reliably.", file=out)
        else:
            print(f"⚡ feval is {result['eval_speedup']:.2f}x faster than BFS", file=out)

        return out.getvalue()


    def format_summary(self, stats: dict) -> str:
        """
        Format the overall summary of all test cases.

        Includes:
          - Total number of tests run.
          - Number of failed tests.
          - Total number of fallbacks.
          - Average timing for KnightQuest, BFS, and feval.
          - Average speedups.

        Args:
            stats (dict): A dictionary of summary statistics.

        Returns:
            str: Formatted string of summary results.
        """
        out = StringIO()

        print("\n🧾 Summary:", file=out)

        if 'max_coord' in stats:
            print(f"  Tested over the range:({-stats['max_coord']}, {stats['max_coord']})", file=out)
        if 'seed' in stats:
            print(f"  Seed: {stats['seed']}", file=out)

        print(f"  Total test runs: {stats['total_tests']}", file=out)
        print(f"  Failed tests: {stats['failed_tests']}", file=out)
        print(f"  Total fallback moves used: {stats['total_fallbacks']}", file=out)

        print(f"  Average KQ path time: {stats['avg_kq_time']:.8f}s", file=out)
        print(f"  Average BFS path time: {stats['avg_bfs_time']:.8f}s", file=out)
        print(f"  Average feval time: {stats['avg_eval_time']:.8f}s", file=out)
        
        print(f"  Average KQ speedup: {stats['avg_kq_speedup']:.2f}x", file=out)
        print(f"  Average feval speedup: {stats['avg_eval_speedup']:.2f}x", file=out)

        return out.getvalue()


    def write_to_file(self, results: list[dict], summary: dict, path: str) -> None:
        """
        Write all test case results and the final summary to a specified file.

        Args:
            results (list[dict]): List of result dictionaries from individual test cases.
            summary (dict): Aggregated statistics across all test cases.
            path (str): File path to write the output.
        """
        with open(path, "w", encoding="utf-8") as f:
            
            for result in results:
                f.write(self.format_case_result(result))

            f.write(self.format_summary(summary))