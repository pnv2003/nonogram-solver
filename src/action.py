class Action:
    
    def __init__(self, level, block_id, pos) -> None:
        self.level = level
        self.block_id = block_id
        self.pos = pos
        
    def __repr__(self) -> str:
        return "<Action level={} id={} pos={}>".format(self.level, self.block_id, self.pos)