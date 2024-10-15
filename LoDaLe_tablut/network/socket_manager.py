import socket

class SocketManager:
    def __init__(self, ip, port):
        self._ip = ip
        self._port = port
        self._sock = None
        
    def create_socket(self):
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def bind_socket(self):
        try:
            self._sock.bind((self._ip, self._port))
        except socket.error as e:
            self._sock.close()
            print(e)
            exit(1) 