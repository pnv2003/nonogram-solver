import time
import tkinter as tk
import tracemalloc

from src.gen import Gen
from src.puzzle import Nonogram
from src.search import DFS, BeFS
from src.state import State
from src.utils import heuristic_level
NONOGRAM_BOARD_SIZE = 5
DEFAULT_FONT = "TkDefaultFont"
DEFAULT_BACKGROUND = "SystemButtonFace"

# ---
grid = [
        [1, 1, 1, 0, 0],
        [0, 0, 0, 0, 1],
        [1, 0, 0, 1, 1],
        [0, 1, 0, 0, 1],
        [1, 0, 1, 0, 1]
]

# grid = Gen.gen_grid(NONOGRAM_BOARD_SIZE)
init = State(size=NONOGRAM_BOARD_SIZE, num=Gen.gen_grid_num(grid))
puzzle = Nonogram(init)
row_hints = init.row_num
col_hints = init.col_num
algo = "DFS"
# ---

# layout: window
window = tk.Tk()
window.title("Nonogram Puzzle Solver")
window.columnconfigure(index=0, minsize=200)
window.columnconfigure(index=1, minsize=500)
window.resizable(width=False, height=False)

frame_left = tk.Frame(master=window)
frame_right = tk.Frame(master=window)
frame_right.rowconfigure(index=0, minsize=100)
frame_right.rowconfigure(index=1, minsize=250)
frame_right.rowconfigure(index=2, minsize=100)

frame_left.grid(row=0, column=0)
frame_right.grid(row=0, column=1)

# layout: state variables (left)
frame_env = tk.Frame(master=frame_left)
frame_algo = tk.Frame(master=frame_left)

frame_env.grid(row=0, column=0, pady=20)
frame_algo.grid(row=1, column=0, pady=20)

states = [
    'level',
    'start',
    'block_id',
    'level_done',
    'remaining_levels',
    'invalid'
]
label_states = dict()

for i, state in enumerate(states):
    label_name = tk.Label(master=frame_env, text=state)
    label_value = tk.Label(master=frame_env, text=getattr(init, state))
    label_name.grid(row=i, column=0, sticky="w", padx=10)
    label_value.grid(row=i, column=1, sticky="w", padx=10)
    label_states[state] = label_value
    
label_time = tk.Label(master=frame_env, text="time")
label_time_value = tk.Label(master=frame_env, text="")
label_mem = tk.Label(master=frame_env, text="memory")
label_mem_value = tk.Label(master=frame_env, text="")

label_time.grid(row=7, column=0, sticky="w", padx=10)
label_time_value.grid(row=7, column=1, sticky="w", padx=10)
label_mem.grid(row=8, column=0, sticky="w", padx=10)
label_mem_value.grid(row=8, column=1, sticky="w", padx=10)

def switch_algo():
    global algo
    if algo == "DFS":
        algo = "BeFS"
        button_algo["text"] = "BeFS"
    else:
        algo = "DFS"
        button_algo["text"] = "DFS"
        
button_algo = tk.Button(master=frame_algo, text=algo, font=(DEFAULT_FONT, 25), command=switch_algo)
button_algo.grid(row=0, column=0, ipadx=10, ipady=10)


# layout: output and controller (right)
frame_board = tk.Frame(master=frame_right)
frame_board.columnconfigure(
    index=list(range(NONOGRAM_BOARD_SIZE + 1)),
    minsize=50
)
frame_board.rowconfigure(
    index=list(range(NONOGRAM_BOARD_SIZE + 1)),
    minsize=50
)
frame_message = tk.Frame(master=frame_right)
frame_control = tk.Frame(master=frame_right)

frame_message.grid(row=0, column=0)
frame_board.grid(row=1, column=0)
frame_control.grid(row=2, column=0)

# message

label_message = tk.Label(master=frame_message, text="Press 'Solve' to get the solution!", font=(DEFAULT_FONT, 12))
label_message.grid(row=0, column=0, sticky="ew")

# ---
frame_rowlabels = [
    None    
    for i in range(NONOGRAM_BOARD_SIZE)
]

frame_collabels = [
    None
    for i in range(NONOGRAM_BOARD_SIZE)
]

frame_incells = [
    [
        None
        for j in range(NONOGRAM_BOARD_SIZE)    
    ]
    for i in range(NONOGRAM_BOARD_SIZE)
]
# ---

# board

for i in range(NONOGRAM_BOARD_SIZE):
    
    frame_rowlabel = tk.Frame(master=frame_board)
    frame_rowlabel.grid(row=i+1, column=0, sticky="e", padx=10)
    frame_rowlabels[i] = frame_rowlabel
    
    for idx, hint in enumerate(row_hints[i]):
        label_hint = tk.Label(master=frame_rowlabel, text=hint, font=(DEFAULT_FONT, 16))
        label_hint.grid(row=0, column=idx, sticky="ns")
        
    frame_collabel = tk.Frame(master=frame_board)
    frame_collabel.grid(row=0, column=i+1, sticky="s", pady=10)
    frame_collabels[i] = frame_collabel
    
    for idx, hint in enumerate(col_hints[i]):
        label_hint = tk.Label(master=frame_collabel, text=hint, font=(DEFAULT_FONT, 16))
        label_hint.grid(row=idx, column=0, sticky="ew")
        
    for j in range(NONOGRAM_BOARD_SIZE):
        
        frame_cell = tk.Frame(master=frame_board, borderwidth=1, relief="solid")
        frame_cell.grid(row=i+1, column=j+1, sticky="nsew")
        
        frame_cell.rowconfigure(index=0, weight=1)
        frame_cell.columnconfigure(index=0, weight=1)
        
        frame_incell = tk.Frame(master=frame_cell, background=DEFAULT_BACKGROUND, width=42, height=42)
        frame_incell.grid(row=0, column=0)
        
        frame_incells[i][j] = frame_incell

# controller

index = None
trace = None

def display(idx: int):
    
    if idx == len(trace) - 1:
        button_next["state"] = "disabled"
        button_skip["state"] = "disabled"
    else:
        button_next["state"] = "normal"
        button_skip["state"] = "normal"
        
    if idx == 0:
        button_prev["state"] = "disabled"
    else:
        button_prev["state"] = "normal"
    
    current = trace[idx]
    
    # action    
    if not current.parent:
        label_message["text"] = "Puzzle solved!"
    elif current.parent.state.level_done:
        label_message["text"] = f"Switch to level {current.action.row}"
    else:
        label_message["text"] = f"Insert block of size {current.action.size} at ({current.action.row}, {current.action.col})"
    
    if idx == len(trace) - 1:
        label_message["text"] += ". Reached the goal!"
    
    # grid
    grid = current.state.grid
    for i in range(NONOGRAM_BOARD_SIZE):
        for j in range(NONOGRAM_BOARD_SIZE):
            if grid[i][j] == 1:
                frame_incells[i][j]['background'] = 'black'
            else:
                frame_incells[i][j]['background'] = DEFAULT_BACKGROUND
                
    # state variables
    for state in states:
        label_states[state]["text"] = getattr(current.state, state)

def gen():
    label_message["text"] = "Please restart the app to generate another input :)"

def solve():
    global trace, index
    
    start_time = time.time()
    if algo == "DFS":
        node, trace = DFS(puzzle, trace=True)
    else:
        node, trace = BeFS(puzzle, heuristic_level, trace=True)
    end_time = time.time()
    
    tracemalloc.start()
    if algo == "DFS":
        node, trace = DFS(puzzle, trace=True)
    else:
        node, trace = BeFS(puzzle, heuristic_level, trace=True)
    cur, mem = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    
    label_time_value["text"] = f"{round(end_time - start_time, 6)} seconds"
    label_mem_value["text"] = f"{round(mem / 1024**2, 6)} MB"
    
    label_message["text"] = "Puzzle solved!"
    index = 0
    display(index)

def prev():
    global index
    index -= 1
    display(index)

def next(loop=False):
    global index
    if (index >= len(trace)):
        label_message["text"] = "Goal reached!"
        button_next["state"] = "disabled"
    else:        
        index += 1
        display(index)
        
    if loop and index < len(trace) - 1:
        window.after(200, next, True)
    
def skip():
    global index
    index = len(trace) - 1
    display(index)
    
def run():
    label_message["text"] = "Running the solution..."
    solve()
    next(loop=True)
    
button_gen = tk.Button(master=frame_control, text="Generate", command=gen)
button_solve = tk.Button(master=frame_control, text="Solve", command=solve)
button_run = tk.Button(master=frame_control, text="Run", command=run)
button_next = tk.Button(master=frame_control, text="Next Step", command=next, state="disabled")
button_prev = tk.Button(master=frame_control, text="Previous Step", command=prev, state="disabled")
button_skip = tk.Button(master=frame_control, text="Skip", command=skip, state="disabled")

button_gen.grid(row=0, column=0, ipadx=10, ipady=10)
button_solve.grid(row=0, column=1, ipadx=10, ipady=10)
button_run.grid(row=0, column=2, ipadx=10, ipady=10)
button_prev.grid(row=0, column=3, ipadx=10, ipady=10)
button_next.grid(row=0, column=4, ipadx=10, ipady=10)
button_skip.grid(row=0, column=5, ipadx=10, ipady=10)
        
window.mainloop()
    



