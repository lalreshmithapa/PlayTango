import argparse
from manual.play import main as manual_main
from solvers.astar import main as astar_main
from solvers.ac3 import main as ac3_main
from solvers.qlearn import main as qlearn_main
def main():
    parser = argparse.ArgumentParser(description="Tango Puzzle Game")
    parser.add_argument("-m", "--mode", choices=["manual", "astar", "ac3", "qlearn"], required=True,
                        help="Choose mode: manual (human play), astar (A* solving), ac3 (AC-3 with backtracking), qlearn (Q-Learning)")
    args = parser.parse_args()

    if args.mode == "manual":
        manual_main()
    elif args.mode == "astar":
        astar_main()
    elif args.mode == "ac3":
        ac3_main()
    elif args.mode == "qlearn":
        qlearn_main()

if __name__ == "__main__":
    main()
