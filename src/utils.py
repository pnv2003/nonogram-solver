def check_col_arr(curr:list, constr:list) -> bool:
    num_of_list = len(constr) - len(curr) + 1
    for i in range(num_of_list):
        check = True
        for j in range(i,len(curr)):
            if curr[j] > constr[j]: 
                check = False
                break
        curr = [0] + curr
        if len(curr) > len(constr): return check


