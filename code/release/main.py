
import argparse
from model.point import Point
from logic.kq import KnightQuest

def str_to_point(value: str) -> Point:
    """
    Convert a string 'x,y' into a Point instance, handling negative values and stray quotes.
    """
    try:
        value = value.strip().strip('"').strip("'") 
        x, y = map(int, value.split(','))
        return Point(x, y)
    
    except ValueError:
        raise ValueError(f"Invalid point format: '{value}'. Expected format is 'x,y'.")


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Knight pathfinding test runner.")
    parser.add_argument("--start", type=str, default="0,0", help="Starting point[str]: 'x,y'")
    parser.add_argument("--end", type=str, default="10,10", help="Ending point[str]: 'x,y'")
    args = parser.parse_args()

    start = str_to_point(args.start)
    end = str_to_point(args.end)

    print(f"\nStarting point: ({start.x}, {start.y})")
    print(f"Ending point: ({end.x}, {end.y})\n")

    # Get the path and evaluation result
    kq = KnightQuest(start, end)
    eval = kq.feval(start, end)
    path = kq.fpath()

    print(f"Evaluation Result: {eval}")
    print(" -> ".join([f"({p.x}, {p.y})" for p in path]))
