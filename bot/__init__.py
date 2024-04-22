from logs.logger import *

NAME = ""
AVATAR = ""
DESCRIPTION = ""
PREFIX = "!"

VERSION = "0.1"
COLORS = [0x000000, 0xFFFFFF]

GUILD_ID = 0

DEVELOPERS = [0]

with open("./secrets/token", "r") as f:
    TOKEN = f.read().strip()
    f.close()