from copy import deepcopy

from src.gen import Gen

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
        self.start = 0                              # col to insert block
        self.block_id = 0                           # block to be inserted
        
        # custom level order
        self.remaining_levels = set(range(self.height))
        self.level_done = False
        
        # validity
        self.invalid = False                        # current grid state is invalid or not
    
    def current_block_size(self):
        return self.row_num[self.level][self.block_id]
    
    def out_of_range(self, row, col):
        if 0 <= row < self.height and 0 <= col <= self.width:
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
            
        # state switch
        state.start = col + size + 1
        
        state.block_id += 1
        if state.block_id >= len(state.row_num[state.level]):
            state.level += 1
            state.start = 0
            state.block_id = 0
            
        if state.level >= state.height:
            state.invalid = True
            
        return state
    
    def switch_level(self, level):
        
        if not self.level_done:
            raise Exception("Unexpected Error: Switching from an undone level")
        
        state = deepcopy(self)
        
        state.level_done = False
        state.remaining_levels.remove(state.level)
        state.level = level
        state.start = 0
        state.block_id = state.row_num[level][0]
        
        return state
    
    def test(self):
        # print(f"Test state:\n {self}\n")
        return (self.num == Gen.gen_grid_num(self.grid))
    
    def __repr__(self) -> str:
        return "\n" + Gen.grid_str(self.grid) + "\n"
        
    
    