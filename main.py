import cmd
import os
from tabulate import tabulate
from modules.CORE import C2core


class PiratesStrike(cmd.Cmd):
    prompt = "$> "
    core = C2core()
    payloads = core.ListAll("payloads")
    CurrentPayload = None


    def preloop(self):
        null = 0
        settings = self.core.ListAll("settings")
        for attr in settings.keys():
            if settings[attr] is None:
                print(f"[!] {attr.upper()} is null")
                null += 1

        if null != 0:
            print("\n[+] use the set command to update the null attributes before starting.")

    def do_exit(self, arg):
        exit(0)

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
        "show the available payloads or current settings.\n"
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
        "save the current settings\n"
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


if __name__ == '__main__':
    try:
        PiratesStrike().cmdloop()
    except KeyboardInterrupt:
        pass