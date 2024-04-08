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
        
        constraint = state.constraint_states
        levels = list(state.unsatisfied)
        
        return [
            Action(level, id, pos)
            for level in levels
            for id in constraint[level].get_unpicked_blocks()
            for pos in constraint[level].get_range(id)
        ]    
    
    def result(self, state: State, action: Action):
        return state.insert(action.level, action.block_id, action.pos)
    
    def goal_test(self, state: State):
        return state.test()
    
    
        
    
    