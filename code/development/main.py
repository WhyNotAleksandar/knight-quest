
import argparse
from tests.tester import KnightPathTester

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Knight pathfinding test runner.")

    parser.add_argument("--num_cases", type=int, default=100,
                        help="Number of test cases to generate (default: 100)")
    parser.add_argument("--max_coord", type=int, default=100,
                        help="Point range: (-max_cord, +max_coord) (default: 100)")
    parser.add_argument("--seed", type=int, default=None,
                        help="Random seed for reproducibility (default: None)")
    parser.add_argument("--log", choices=["console", "file"], default="console",
                        help="Output mode: 'console' or 'file' (default: console)")
    parser.add_argument("--path", type=str, default="tests/output/log.txt",
                        help="File path to write results if --log=file (default: tests/output/log.txt)")

    args = parser.parse_args()

    tester = KnightPathTester(args.num_cases, args.max_coord, args.seed)

    if args.log == "file":
        tester.run_all_file(args.path)
    else:
        tester.run_all_console()
