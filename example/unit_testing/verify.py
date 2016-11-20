import sys

command = sys.argv[1]
output = sys.argv[2]
code = int(sys.argv[3])

if ' ' in command:
    nums = command.split(' ')[1:]
    if len(nums) == 2:
        res = str(int(nums[0]) + int(nums[1]))
        if res == output:
            sys.exit(0)
        else:
            sys.exit(1)
if code == 84:
    sys.exit(0)
else:
    sys.exit(2)
