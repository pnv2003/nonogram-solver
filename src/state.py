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
        self.level = 0                              # row to insert block
        while self.level < self.height and self.row_num[self.level][0] == 0: # skip empty rows
                self.level += 1
        self.start = 0                              # col to insert block
        self.block_id = 0                           # block to be inserted
        
        # for fast checking column constraints
        self.column_major_grid = [
            [ 0 for r in range(self.height)]
            for c in range(self.width)
        ]
        
        # validity
        self.invalid = False                        # current grid state is invalid or not
    
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
        
    # def fill(self, row, col):
        
    #     state = deepcopy(self)
        
    #     if self.out_of_range(row, col):
    #         raise Exception("Out of range")
    #     if self.filled(row, col):
    #         raise Exception("Fill a filled cell")
        
    #     state.grid[row][col] = 1
    #     return state
    
    def insert(self, row, col, size):
        
        # print(f"Inserting block {size} at {row}, {col}")
        
        if self.out_of_range(row, col) or self.out_of_range(row, col + size - 1):
            raise Exception("Out of range")
        
        state = deepcopy(self)
        
        for i in range(col, col + size):
            if self.filled(row, i):
                raise Exception("Fill a filled cell")
            state.grid[row][i] = 1
            
            # TODO: check column constraint (possible speed-up)
            current_num = Gen.gen_grid_num_arr(state.column_major_grid[i])
            if not utils.check_col_arr(current_num, state.col_num[i]):
                # print("Column constraint mismatch:")
                # print(f"Column: {state.column_major_grid[i]}")
                # print(f"Current: {current_num}")
                # print(f"Constraint: {state.col_num[i]}\n")
                
                state.invalid = True
            else:
                state.column_major_grid[i][row] = 1
            
        # state switch
        state.start = col + size + 1
        
        state.block_id += 1
        if state.block_id >= len(state.row_num[state.level]):
            state.level += 1
            while state.level < state.height and state.row_num[state.level][0] == 0: # skip empty rows
                state.level += 1
            state.start = 0
            state.block_id = 0
            
        if state.level >= state.height:
            state.invalid = True
            
        return state
    
    def test(self):
        # print(f"Test state:\n {self}\n")
        return (self.num == Gen.gen_grid_num(self.grid))
    
    def __repr__(self) -> str:
        return "\n" + Gen.grid_str(self.grid) + "\n"
        
    
    