# PirateFury
### Introduction
PirateFury is a C2 server written in Python and comes with payloads written in C, the C2 server has only windows payloads for now.
### Installation
##### 1: clone the repo <br/>
```powershell
git clone https://github.com/yo-aiv1/PirateFury.git
```
##### 2: install requirments <br/>
```powershell
pip install -r requirements.txt
```
##### 3: launch the CLI by running main.py <br/>
```powershell
python main.py
```
### Usage
before you start make sure to add your IP and PORT for the listener and the compiler too using the command `set`, then you can use command `build` and pass the architecture of the executable you want (64 or 32), after that you can use `listen` to listen for upcoming connections.
there are other commands like `load` and `save` for loading and saving settings, use command `help` to list the commands and pass a command to it for more information.
