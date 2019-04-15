import os
def clear():
    os.system('cls' if os.name=='nt' else 'clear')
def print_logo():
    print('_'*line_width)
    print(logo)
    print('_'*line_width)
logo = """
  ___ _         _   ___ _  _
 / __| |_  __ _| |_| __| \\| |
 \\__ \\ ' \\/ _` | / / _|| .` |
 |___/_||_\\__,_|_\\_\\___|_|\\_|
"""
line_width = 60
key = 348397765106765
