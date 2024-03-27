import socket
import time
from tqdm import tqdm

class server():

    def __init__(self, ip: str, port: int):
        self.ip = ip
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.ip, self.port))
        self.socket.listen(5)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)

    def GetConnections(self, seconds=10) -> list:
        AliveAgents = []
        self.socket.settimeout(seconds + 1)
        try:
            while True:
                client_socket, addr = self.socket.accept()
                AliveAgents.append(client_socket)
        except socket.timeout:
            return AliveAgents

    def PrintLoadingBar(self, seconds) -> None:
        for i in tqdm(range(int(seconds / 0.1))):
            time.sleep(0.1)

    def kill(self) -> bool:
        pass


