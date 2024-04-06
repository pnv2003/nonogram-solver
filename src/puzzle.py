from src.state import State
from src.problem import Problem

class Nonogram(Problem):
    
    def __init__(self, initial: State = None):
        
        self.initial = initial or State()
        self.height = initial.height
        self.width = initial.width
        
        self.squares = {
            (row, col)
            for row in range(initial.height)
            for col in range(initial.width)
        }
        
    def actions(self, state: State):
        return list(self.squares - state.filled_squares)
    
    def result(self, state: State, action: tuple):
        new = state.fill(*action)
        return new
    
    def goal_test(self, state: State):
        return state.test()
    
    
        
    
    