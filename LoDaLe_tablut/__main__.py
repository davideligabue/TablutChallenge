import sys
from network.socket_manager import SocketManager

PORT = {"white":5800, "black":5801}

def main():
    if len(sys.argv) < 3:
        print("Utilizzo: python script.py <color(White/Black)> <timeout(seconds)> <IP_server>")
        sys.exit(1)
    
    color = sys.argv[1].lower()
    timeout = sys.argv[2]
    ip = sys.argv[3]            # TODO: check if string format is ok for SocketManager
    port = PORT[color]

    s = SocketManager(ip, port)
    s.create_socket()
    s.bind_socket()
    
    pass
    


if __name__ == "__main__":
    main()