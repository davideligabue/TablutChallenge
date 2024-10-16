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
    
def check_timeout(target_time):
    '''
    Checks if the timeout is terminated or not
    
    NB: Assume target_time = time.time() + timeout(s)
    '''
    diff = target_time - time.time()
    if (diff <= 0) :
        raise Exception(f"Timeout expired: {diff:4f}s")
