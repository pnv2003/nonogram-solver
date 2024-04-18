import os
from src.gen import Gen
from src.puzzle import Nonogram
from src.state import State

import time
import tracemalloc
from src.search import BeFS
from src.search import DFS
from src.utils import heuristic_col
from src.utils import heuristic_level

grid_5_1 = [
        [1, 1, 0, 1, 1],
        [0, 1, 0, 0, 0],
        [0, 1, 1, 1, 0],
        [1, 0, 0, 0, 0],
        [1, 0, 1, 1, 0]
]

grid_5_2 = [
        [1, 1, 1, 0, 0],
        [0, 0, 0, 0, 1],
        [1, 0, 0, 1, 1],
        [0, 1, 0, 0, 1],
        [1, 0, 1, 0, 1]
]

grid_6_1 = [
        [0, 1, 0, 1, 1, 1],
        [0, 1, 1, 0, 1, 1],
        [1, 1, 0, 1, 0, 0],
        [1, 0, 0, 0, 1, 0],
        [0, 1, 0, 1, 0, 0],
        [1, 0, 1, 0, 1, 0]
]

grid_6_2 = [
        [0, 0, 0, 1, 1, 1],
        [0, 1, 0, 0, 1, 0],
        [0, 1, 1, 1, 1, 1],
        [1, 0, 1, 0, 1, 0],
        [0, 1, 0, 0, 0, 1],
        [1, 0, 0, 1, 1, 0]
]

grid_7_1 =[
    [1, 1, 1, 0, 1, 0, 1],
    [1, 1, 1, 0, 1, 1, 0],
    [0, 0, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 0, 0, 1],
    [0, 1, 0, 0, 1, 0, 1],
    [1, 0, 0, 1, 0, 0, 1],
]

grid_7_2 = [
    [0, 0, 1, 1, 0, 1, 1],
    [0, 1, 0, 0, 1, 1, 1],
    [0, 0, 0, 1, 1, 0, 0],
    [1, 0, 0, 0, 0, 0, 1],
    [1, 1, 0, 0, 0, 1, 1],
    [1, 0, 1, 1, 0, 0, 0],
    [1, 0, 1, 1, 1, 0, 1],
]

grid_list = [grid_5_1 , grid_5_2 , grid_6_1 , grid_6_2 , grid_7_1 , grid_7_2]

i = 1

if not os.path.exists('./output'):
    os.mkdir('./output')
for grid in grid_list:
    # For initing a random puzzle with size
    # init = State(size=5)

    init = State(len(grid), num=Gen.gen_grid_num(grid))
    puzzle = Nonogram(init)
    ##################################
    # DFS
    ## Time Elapsed
    start_time = time.time()

    solution_DFS = DFS(puzzle)

    elapsed_time = time.time() - start_time
    print('testcase ' + str(i) + ': size = ' + str(len(grid)) + '\n')
    print('DFS:')

    print(f"Time taken: {round(elapsed_time, 6)} seconds")

    ## Memory Usage
    tracemalloc.start()

    solution_DFS = DFS(puzzle)

    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    current /= 1024**2
    peak /= 1024**2
    
    
    print(f"Memory usage: current is {round(current, 6)} MB, peak was {round(peak, 6)} MB")
#     print(f"\nDFS Solution:")
#     print(solution.path())
    print()
    ##################################
    # BeFS with Level Heuristic
    start_time = time.time()

    solution_BeFS_1 = BeFS(puzzle,heuristic_level)

    elapsed_time = time.time() - start_time

    print('BeFS with Level Heuristic:')

    print(f"Time taken: {round(elapsed_time, 6)} seconds")

    ## Memory Usage
    tracemalloc.start()

    solution_BeFS_1 = BeFS(puzzle,heuristic_level)

    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    current /= 1024**2
    peak /= 1024**2

    print(f"Memory usage: current is {round(current, 6)} MB, peak was {round(peak, 6)} MB")
    # print(f"\nDFS Solution:")
    # print(solution.path())
    print()
    ##################################
    # BeFS with Column Heuristic
    # start_time = time.time()

    # solution_BeFS_2 = BeFS(puzzle,heuristic_col)

    # elapsed_time = time.time() - start_time

    # print('BeFS with Column Heuristic:')

    # print(f"Time taken: {round(elapsed_time, 6)} seconds")

    # ## Memory Usage
    # tracemalloc.start()

    # solution_BeFS_2 = BeFS(puzzle,heuristic_col)

    # current, peak = tracemalloc.get_traced_memory()
    # tracemalloc.stop()

    # current /= 1024**2
    # peak /= 1024**2

    # print(f"Memory usage: current is {round(current, 6)} MB, peak was {round(peak, 6)} MB")
    # # print(f"\nDFS Solution:")
    # # print(solution.path())
    # print()
    
    with open('output/tc'+ str(i) + '.txt','w') as f:
        f.write('testcase '+ str(i) + ': size = ' + str(len(grid)) + '\n')
        f.write('DFS:' + '\n')
        f.write(str(solution_DFS.path()))
        f.write('\n\n')
        f.write('BeFS with Column Heuristic:' + '\n')
        f.write(str(solution_BeFS_1.path()))
        f.write('\n\n')
        # f.write('BeFS with Column Heuristic:' + '\n')
        # f.write(str(solution_BeFS_2.path()))
        # f.write('\n\n')
    i += 1    
    
    