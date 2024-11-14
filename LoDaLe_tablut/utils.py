import ipaddress
import time
from collections import Counter
import numpy as np

def check_ip(ip):
    '''
    Checks if the IP address is well-formatted
    '''
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False
    
def check_timeout(start_time, timeout):
    if time.time() - start_time > timeout:
                raise TimeoutError("Timeout reached")

# def pretty_print(board):
#     # Board dimension
#     n = board.shape[0]
    
#     # Literal labels (A, B, C, ...)
#     column_labels = '    ' + '   '.join([chr(i + ord('A')) for i in range(n)])  # Quattro spazi
#     print(column_labels)
    
#     # Separators
#     separator = '  ' + '+---' * n + '+'
    
#     for i in range(n):
#         print(separator)
        
#         # Row + pieces
#         row = f'{i+1:2d} ' + '|'.join([f' {cell[0]} ' if cell != 'EMPTY' else '   ' for cell in board[i]]) + ' |'
#         print(row)
    
#     print(separator)
    
def tuple2alfanum(tuple_pos):
    row, col = tuple_pos
    col_alfnum = chr(ord('a') + col)
    row_alfnum = str(1+row)
    return col_alfnum + row_alfnum

def alfnum2tuple(alfnum_pos):
    col_alfnum, row_alfnum = tuple(alfnum_pos)
    col_tuple = ord(col_alfnum) - ord('a')
    row_tuple = int(row_alfnum) - 1
    return (row_tuple, col_tuple)

def get_n_most_winning_move(dataset, results, n, color):

    # Filter idxs
    max_turns = max([len(match) for match in dataset])
    if color[0]=="W" :
        possible_idx = [2*i for i in range(max_turns)]   
    else :
        possible_idx = [2*i+1 for i in range(max_turns)]
    
    idx = possible_idx[n]          # which move (column)

    idx_moves = []
    for i, match in enumerate(dataset) :
        try:
            if results[i]==color[0] : # if wins
                idx_moves.append(tuple(match[idx]))
        except: continue
        
    move_counter = Counter(idx_moves)
    most_common_moves = move_counter.most_common(None) # all the results
    return most_common_moves

def cells_on_line(x0, y0, x1, y1):
    """
    Returns the cells in the line among (x0, y0) and (x1, y1). 
    (using Bresenham algorithm) 
    """
    
    cells = []
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx - dy

    while True:
        cells.append((x0, y0))
        if x0 == x1 and y0 == y1:
            break
        e2 = err * 2
        if e2 > -dy:
            err -= dy
            x0 += sx
        if e2 < dx:
            err += dx
            y0 += sy

    return cells

if __name__ == "__main__":
    matrix = np.ones((5,5))
    cells = cells_on_line(
            x0=0,y0=0,
            x1=2,y1=4
        )
    for i in range(5):
        for j in range(5):
            if (i,j) in cells : matrix[i][j] = 0
        
    # print(cells_on_line(2,2,0,0))
    print(matrix)