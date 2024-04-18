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
        
        if state.level_done or state.level is None:
            
            # print(f"Expanding state: {state}")
            
            remains = list(state.remaining_levels)
            remains.reverse()
            actions = [
                Action(level, 0, 0) # only level are sent
                for level in remains
                if state.row_num[level][0] != 0 # skip empty row
            ]
            
            return actions
        
        level = state.level
        start = state.start
        size = state.current_block_size()
        
        # Ex: Fit 2 -> # # . _ _ _ _
        #                    ^ ^ ^
        end = state.width - size
        
        # speed boost: end limitation
        for id in range(state.block_id + 1, len(state.row_num[level])):
            block = state.row_num[level][id]
            end -= block + 1
        
        return [
            Action(level, i, size)
            # for i in range(start, end + 1)
            for i in range(end, start - 1, -1)
        ]    
    
    def result(self, state: State, action: Action):
        
        new = None
        if state.level_done or state.level is None:
            new = state.switch_level(action.row)
            new.prune = True # prune all other levels
        else:
            new = state.insert(action.row, action.col, action.size)
            new.prune = False # stop pruning
        return new
    
    def goal_test(self, state: State):
        return state.test()
    
    
        
    
    