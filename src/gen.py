import random

from numpy import array_str 
class Gen:
    @staticmethod    
    def gen_grid(size = 5):
        black_squares = int (size*size*0.5)
        count = 0
        grid = []
        for i in range(size):
            col = []
            for j in range(size):
                col.append(0)
            grid.append(col)
        while count < black_squares:
            rand_col = random.randint(0,size-1)
            rand_row = random.randint(0,size-1)
            if grid[rand_row][rand_col] == 0:
                grid[rand_row][rand_col] = 1
                count += 1
        return grid
    
    @staticmethod
    def gen_grid_num_arr(in_arr):
        size = len(in_arr)
        out_arr = []
        count_in_row = 0
        for i in range(size):
            if in_arr [i]== 1 :
                count_in_row += 1
            else:
                if count_in_row != 0:
                    out_arr.append(count_in_row)
                count_in_row = 0
        if count_in_row != 0:
            out_arr.append(count_in_row)
        elif count_in_row == 0 and len(out_arr) == 0 :
            out_arr.append(count_in_row)
        return out_arr

    @staticmethod
    def gen_grid_num(grid):
        size = len(grid)
        row_num = []
        col_num = []
        col = []
        for i in range(size):
            row_num.append(Gen.gen_grid_num_arr(grid[i]))
            col_arr = []
            for j in range(size):
                col_arr.append(grid[j][i])
            col.append(col_arr)
        for i in range(size):
            col_num.append(Gen.gen_grid_num_arr(col[i]))
        grid_num =  row_num + col_num
        return grid_num

    @staticmethod
    def print_grid(grid):
        size = len(grid)
        # for row in grid:
        #     print(row)
        
        grid_num = Gen.gen_grid_num(grid)
        for i in range(size):       
            row_str ="  ".join(['#' if j == 1 else '.' for j in grid[i]])
            row_str += "    "
            for j in grid_num[i]:
                row_str += str(j) + ' '
            print(row_str)
        print("")
        max_len = 0
        for i in range(size):
            if len(grid_num[i+size]) > max_len: max_len = len(grid_num[i+size])

        for i in range(max_len):
            lrow_str =''
            for j in range(size):
                if i >= len(grid_num[j+size]):
                    lrow_str += '   '
                else:
                    lrow_str += str(grid_num[j+size][i]) + '  '
            print(lrow_str)
        
    @staticmethod
    def gen_num(size):
        return Gen.gen_grid_num(Gen.gen_grid(size))
        





         
