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
        self.filled_squares = set()
    
    def out_of_range(self, row, col):
        if 0 <= row < self.width and 0 <= col <= self.height:
            return False
        return True
    
    def filled(self, row, col):
        if self.out_of_range(row, col):
            raise Exception("Out of range")
        return self.grid[row][col] == 1
        
    def fill(self, row, col):
        
        state = deepcopy(self)
        
        if self.out_of_range(row, col):
            raise Exception("Out of range")
        if self.filled(row, col):
            raise Exception("Fill a filled cell")
        
        state.grid[row][col] = 1
        state.filled_squares.add((row, col))
        return state
    
    def test(self):
        return (self.num == Gen.gen_grid_num(self.grid))
    
    def __repr__(self) -> str:
        return "<State>\n" + Gen.grid_str(self.grid) + "\n"
        
    
    