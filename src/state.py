from copy import deepcopy
from src.gen import Gen
import src.utils as utils

class State:
    
    def __init__(self, size=5, num=None) -> None:
        self.width = size
        self.height = size
        self.grid = [
            [ 0 for c in range(self.width) ]
            for r in range(self.height)
        ]
        
        self.num = num or Gen.gen_num(size)
        self.row_num = self.num[:self.height]
        self.col_num = self.num[self.height:]
        
        # additional state attributes
        
        # action-related states
        self.level = None                           # row to insert block
        self.start = 0                              # col to insert block
        self.block_id = 0                           # block to be inserted
        
        # custom level order
        self.remaining_levels = set(range(self.height))
        self.level_done = False
        
        # for fast checking column constraints
        # self.column_major_grid = [
        #     [ 0 for r in range(self.height)]
        #     for c in range(self.width)
        # ]
        
        # validity
        self.invalid = False                        # current grid state is invalid or not
        
        # support pruning
        self.prune = False
    
    def current_block_size(self):
        return self.row_num[self.level][self.block_id]
    
    def out_of_range(self, row, col):
        if 0 <= row < self.height and 0 <= col < self.width:
            return False
        return True
    
    def filled(self, row, col):
        if self.out_of_range(row, col):
            raise Exception("Out of range")
        return self.grid[row][col] == 1
    
    def insert(self, row, col, size):
        
        # print(f"Inserting block {size} at {row}, {col}")
        
        state = deepcopy(self)
        
        if self.out_of_range(row, col) or self.out_of_range(row, col + size - 1):
            raise Exception("Out of range")
        
        for i in range(col, col + size):
            if self.filled(row, i):
                raise Exception("Fill a filled cell")
            state.grid[row][i] = 1
            
            # TODO: check column constraint (possible speed-up)
            
            # current_num = Gen.gen_grid_num_arr(state.column_major_grid[i])
            # if not utils.check_col_arr(current_num, state.col_num[i]):
            #     # print("Column constraint mismatch:")
            #     # print(f"Column: {state.column_major_grid[i]}")
            #     # print(f"Current: {current_num}")
            #     # print(f"Constraint: {state.col_num[i]}\n")
                
            #     state.invalid = True
            # else:
            #     state.column_major_grid[i][row] = 1
            
        # state switch
        state.start = col + size + 1
        state.block_id += 1
        
        # reached new level
        if state.block_id >= len(state.row_num[state.level]):
            state.level_done = True
            state.start = 0
            state.block_id = 0
            
        return state
    
    def switch_level(self, level):
        
        if not self.level_done and self.level is not None:
            raise Exception("Unexpected Error: Switching from an undone level")
        
        state = deepcopy(self)
        
        state.remaining_levels.remove(level)
        state.level_done = False
        state.level = level
        state.start = 0
        state.block_id = 0
        
        return state
    
    def test(self):
        return (self.num == Gen.gen_grid_num(self.grid))
    
    def __repr__(self) -> str:
        return f"\n<State level={self.level} remain={self.remaining_levels}\n" + Gen.grid_str(self.grid) + "\n>\n"
        
    
    