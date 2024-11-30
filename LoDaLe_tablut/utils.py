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

# take a string and a char and returns a list of all the indexes in which the char is found
def find_all(original:str, tofind:str) -> list:
    result = list()
    for i in range(len(original)):
        if original[i] == tofind:
            result.append(i)
    return result

def is_timeout(start_time, timeout, bonus=1) -> bool:
    res = time.time() - start_time > timeout-bonus
    return res