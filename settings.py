import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def clear():
    os.system('cls' if os.name=='nt' else 'clear')

NAME = "pswd"
LOGO = """______                         _ _   _
| ___ \\                       | | \\ | |
| |_/ /_ _ ___ _____      ____| |  \\| |
|  __/ _` / __/ __\\ \\ /\\ / / _` | . ` |
| | | (_| \\__ \\__ \\\\ V  V / (_| | |\\  |
\\_|  \\__,_|___/___/ \\_/\\_/ \\__,_\\_| \\_/
"""
LINE_WIDTH = 60
KEY = 348397765106765
