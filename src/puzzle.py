from copy import deepcopy
from re import S
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
        
        if state.level_done:
            
            return [
                Action(level, 0, 0) # only level are sent
                for level in state.remaining_levels
            ]
        
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
        
        if state.level_done:
            return state.switch_level(action.row)
        
        return state.insert(action.row, action.col, action.size)
    
    def goal_test(self, state: State):
        return state.test()
    
    
        
    
    