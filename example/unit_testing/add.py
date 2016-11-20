import sys

args = sys.argv
if len(args) != 3:
    sys.exit(84)
print(int(args[1]) + int(args[2]), end='')
sys.exit(0)
