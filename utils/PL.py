import json
import re


def PayloadLoader() -> dict:
    file = open("payloads/payloads.json", "r")
    payloads = json.loads(file.read())

    return payloads

def IpAndPort(file: str, ip: str, port: int) -> None:
    with open(file, 'r') as f:
        content = f.read()
        f.close()

    ModifiedVers = re.sub(r'\bPORT_HERE\b', str(port), content)
    ModifiedVers = re.sub(r'\bIP_HERE\b', ip, ModifiedVers)

    with open("rs.c", 'w') as f:
        f.write(ModifiedVers)
        f.close()