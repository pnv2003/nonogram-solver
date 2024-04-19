# Searching Case Study: Nonogram

Clone this repository to get started!

```bash
git clone https://github.com/phuongngo0320/nonogram-ai
cd nonogram-ai
```

# How to use the GUI

Start the GUI app by running `gui.py`:
```bash
python gui.py
```

| Button | Feature |
|-|-|
| Generate | Generate new puzzle (not ready, restart the app to get a new one :D)
| Solve | Solve the puzzle |
| Run | Automatically solve and run the solution step by step |
| Previous Step | Navigate to the previous step of the solution |
| Next Step | Navigate to the next step of the solution |
| Skip | Skip all the steps and see the solution (quickly :) |
| DFS/BeFS | Switch the search algorithm |

The default size of board is 5x5. You can customize it by modifying the following line:

```py
NONOGRAM_BOARD_SIZE = 5
```

We do not recommend playing with any board larger than 7x7 :)

# Performance Testing

Run `main.py` to check out the benchmarks (time and memory) of DFS (Depth First Search) and BeFS (Best First Search)
```bash
python main.py
```

There are six testcases for 5x5, 6x6 and 7x7 boards. After running the above command, the terminal will show the time and memory usage by DFS and BeFS. You can check out the files in `output` to see each step. 

# Acknowledgements

We are highly inspired by the AIMA books and AIMA Python code by Russell and Norvig.

