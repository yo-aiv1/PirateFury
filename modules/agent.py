import socket


class agent:
    def __init__(self, AgentSocket: socket) -> None:
        """Initialize the object.

        Args:
            AgentSocket (socket): connection's socket.
        """
        self.AgentSocket = AgentSocket

    def ExecCmd(self, command: str) -> str:
        """Execute command on an agent.

        Args:
            command (str): command to be executed.

        Returns:
            str: the ouput of the executed command.
        """
        self.AgentSocket.send(command.encode())
        response = self.AgentSocket.recv(1024)

        return response.decode()

    def kill(self) -> None:
        """kill an agent connection."""
        self.AgentSocket.close()
