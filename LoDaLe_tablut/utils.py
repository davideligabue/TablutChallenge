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
    # Dimensioni della scacchiera
    n = board.shape[0]
    
    # Stampa la riga delle coordinate delle colonne (A, B, C, ...)
    column_labels = '    ' + '   '.join([chr(i + ord('A')) for i in range(n)])  # Quattro spazi
    print(column_labels)
    
    # Separatore tra righe
    separator = '  ' + '+---' * n + '+'
    
    for i in range(n):
        # Stampa il separatore
        print(separator)
        
        # Stampa il numero di riga e i pezzi della scacchiera
        row = f'{i+1:2d} ' + '|'.join([f' {cell[0]} ' if cell != 'EMPTY' else '   ' for cell in board[i]]) + ' |'
        print(row)
    
    # Stampa l'ultimo separatore
    print(separator)