from copy import deepcopy

class State:
    
    def __init__(self, height, width) -> None:
        self.width = width
        self.height = height
        self.grid = [
            [ False for c in width ]
            for r in height
        ]
        self.filled_squares = set()
    
    def out_of_range(self, row, col):
        if 0 <= row < self.width and 0 <= col <= self.height:
            return False
        return True
    
    def filled(self, row, col):
        if self.out_of_range(row, col):
            raise Exception("Out of range")
        return self.grid[row][col]
        
    def fill(self, row, col):
        
        grid = deepcopy(self)
        
        if self.out_of_range(row, col):
            raise Exception("Out of range")
        if self.filled(row, col):
            raise Exception("Fill a filled cell")
        
        grid[row][col] = True
        grid.filled_squares.add((row, col))
        return grid
    
    def test(self):
        pass
        
    
    