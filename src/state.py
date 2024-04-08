from copy import deepcopy
from src.debug import dump
from src.gen import Gen
import src.utils as utils

class BlockState:
    
    def __init__(self, size, start=None, end=None) -> None:
        """Block of `size` sit at [`start`, `end`)"""
        
        self.size = size
        self.start = start
        self.end = end
        
    def __repr__(self) -> str:
        return "<Block size={} start={} end={}>".format(self.size, self.start, self.end)
        
class BlockListState:
    
    def __init__(self, space_size, block_sizes) -> None:
        self.space_size = space_size
        self.blocks = [
            BlockState(sz)
            for sz in block_sizes
        ]
        self.unpicked = set([
            id
            for id in range(len(block_sizes))
        ])
        self.count = 0
        
    def pick(self, id, start):
        
        if id not in self.unpicked:
            raise Exception("Unexpected Error: Trying to pick a picked block")
        
        self.blocks[id].start = start
        self.blocks[id].end = start + self.blocks[id].size
        self.unpicked.remove(id)
        self.count += 1
        
    def get_range(self, id):
        
        if id not in self.unpicked:
            raise Exception("Unexpected Error: Trying to get range of a picked block")
        
        start, end = 0, self.space_size
        # find start (go left)
        for i in range(id - 1, -1, -1):
            if i not in self.unpicked:
                start = self.blocks[i].end + 1
                break
        # find end (go right)
        for i in range(id + 1, len(self.blocks)):
            if i not in self.unpicked:
                end = self.blocks[i].start - 1
                break
        
        if start >= end:
            return []
        
        count = end - start - self.blocks[id].size + 1
        end = start + count
        
        # print(f"Got range {start}-{end}")
        return list(range(start, end))
    
    def get_unpicked_blocks(self):
        return list(self.unpicked)
        
    def empty(self):
        return self.count == len(self.blocks)

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
            
        # block-insertion state model
        self.constraint_states = [  
            BlockListState(self.width, sizes)
            for sizes in self.row_num
        ]
        # track unsatisfied constraints
        self.unsatisfied = set([ level for level in range(self.height) ])
        
        self.current_column_numbers = [
            [ 0 for j in range(self.height) ]
            for i in range(self.width)
        ]
        
        # current grid state is invalid or not
        self.invalid = False                        
    
    def out_of_range(self, row, col):
        if 0 <= row < self.height and 0 <= col < self.width:
            return False
        return True
    
    def filled(self, row, col):
        if self.out_of_range(row, col):
            raise Exception("Out of range")
        return self.grid[row][col] == 1
    
    def insert(self, level, block_id, pos):
        
        # print(f"Inserting a block level={level}, id={block_id}, pos={pos}")
        state = deepcopy(self)
        
        block_size = state.row_num[level][block_id]
        
        for i in range(pos, pos + block_size):
            if state.filled(level, i):
                raise Exception("Fill a filled cell")
            state.grid[level][i] = 1
            
            # TODO: check column constraint (possible speed-up)
            if not utils.check_col_arr(
                Gen.gen_grid_num_arr(state.current_column_numbers[i]), 
                state.col_num[i]
            ):
                state.invalid = True
                break
            else:
                state.current_column_numbers[i][level] = 1
            
        # dump(state.grid, "Grid")
            
        # state switch
        state.constraint_states[level].pick(block_id, pos)
        if state.constraint_states[level].empty():
            state.unsatisfied.remove(level)
            
        return state
    
    def test(self):
        # print(f"Test state:\n {self}\n")
        return (self.num == Gen.gen_grid_num(self.grid))
    
    def __repr__(self) -> str:
        return "<State>\n" + Gen.grid_str(self.grid) + "\n"
        
    
    