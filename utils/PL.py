import json
import re


def PayloadLoader() -> dict:
    """Load available payloads

    Returns:
        dict: payloads dict
    """
    file = open("payloads/payloads.json", "r")
    payloads = json.loads(file.read())

    return payloads


def IpAndPort(file: str, ip: str, port: int) -> None:
    """Replace reverse shell code with ip and port.

    Args:
        file (str): reverse shell
        ip (str): ip
        port (int): port
    """
    with open(file, 'r') as f:
        content = f.read()
        f.close()

    ModifiedVers = re.sub(r'\bPORT_HERE\b', str(port), content)
    ModifiedVers = re.sub(r'\bIP_HERE\b', ip, ModifiedVers)

    with open("rs.c", 'w') as f:
        f.write(ModifiedVers)
        f.close()
