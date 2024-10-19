import ipaddress
import time

def check_ip(ip):
    '''
    Checks if the IP address is well-formatted
    '''
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False
    
# def check_timeout(target_time):
#     '''
#     Checks if the timeout is terminated or not
    
#     NB: Assume target_time = time.time() + timeout(s)
#     '''
#     diff = target_time - time.time()
#     if (diff <= 0) :
#         raise Exception(f"Timeout expired: {diff:4f}s")
#     return diff + time.time()

def pretty_print(board):
    # Board dimension
    n = board.shape[0]
    
    # Literal labels (A, B, C, ...)
    column_labels = '    ' + '   '.join([chr(i + ord('A')) for i in range(n)])  # Quattro spazi
    print(column_labels)
    
    # Separators
    separator = '  ' + '+---' * n + '+'
    
    for i in range(n):
        print(separator)
        
        # Row + pieces
        row = f'{i+1:2d} ' + '|'.join([f' {cell[0]} ' if cell != 'EMPTY' else '   ' for cell in board[i]]) + ' |'
        print(row)
    
    print(separator)
    
def tuple2alfanum(tuple_pos):
    row, col = tuple_pos
    col_alfnum = chr(ord('a') + col)
    row_alfnum = str(1+row)
    return col_alfnum + row_alfnum