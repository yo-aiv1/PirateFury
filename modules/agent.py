import socket

class agent:
    def __init__(self, AgentSocket: socket) -> None:
        self.AgentSocket = AgentSocket

    def ExecCmd(self, command: str) -> str:
        self.AgentSocket.send(command.encode())
        response = self.AgentSocket.recv(1024)

        return response.decode()
