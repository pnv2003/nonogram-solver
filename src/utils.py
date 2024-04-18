from src.node import Node
from src.gen import Gen
def check_col_arr(curr:list, constr:list) -> bool:
    # num_of_list = len(constr) - len(curr) + 1
    # for i in range(num_of_list):
    #     check = True
    #     for j in range(i,len(curr)):
    #         if curr[j] > constr[j]: 
    #             check = False
    #             break
    #     curr = [0] + curr
    #     if check == True : return check
    #     if len(curr) > len(constr): return check
    if sum(curr) > sum(constr) : return False
    return True

def heuristic_level(node:Node):
    
    if node.parent.state.level_done:
        row = node.state.row_num[node.state.level]
        size = node.state.width
        priority = (len(row) + 1) ** (size - (sum(row)+(len(row)-1)))
        # priority = (len(row) + 1) ** (size - (sum(row)+(len(row)-1)))
        # return priority
        return -node.depth - 1 / priority
    return -node.depth

def heuristic_col(node:Node):
    state = node.state
    action = node.action
    last_bl_size = action.size
    start_col = action.col
    priority = -1
    for i in range(last_bl_size):
        if check_col_arr(Gen.gen_grid_num_arr(state.column_major_grid[start_col]),
                      state.col_num[start_col]) == False:
            priority = 1
            break
        start_col += 1

    return priority*node.depth
        