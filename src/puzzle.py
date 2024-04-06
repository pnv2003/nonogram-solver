from src.state import State
from src.problem import Problem

class Nonogram(Problem):
    
    def __init__(self, initial=State(5, 5)):
        
        self.height = initial.height
        self.width = initial.width
        self.initial = initial
        
        self.squares = {
            (row, col)
            for row in initial.height
            for col in initial.width
        }
        
    def actions(self, state: State):
        return list(self.squares - state.filled_squares)
    
    def result(self, state: State, action: tuple):
        new = state.fill(*action)
        return new
    
    def goal_test(self, state: State):
        return state.test()
    
    
        
    
    