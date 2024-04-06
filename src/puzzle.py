from src.action import Action
from src.state import State
from src.problem import Problem
    
class Nonogram(Problem):
    
    def __init__(self, initial: State = None):
        
        self.initial = initial or State()
        self.height = initial.height
        self.width = initial.width    
        
    def actions(self, state: State) -> list[Action]:
        
        if state.invalid:
            return []
        
        level = state.level
        start = state.start
        size = state.current_block_size()
        
        # Ex: Fit 2 -> # # . _ _ _ _
        #                    ^ ^ ^
        end = state.width - size
        
        return [
            Action(level, i, size)
            for i in range(start, end + 1)
        ]    
    
    def result(self, state: State, action: Action):
        return state.insert(action.row, action.col, action.size)
    
    def goal_test(self, state: State):
        return state.test()
    
    
        
    
    