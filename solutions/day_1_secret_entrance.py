import os

# Determine the project root directory
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Read input file
with open(os.path.join(root_dir, "inputs", "day_1_input.txt")) as f:
    lines = [line.strip() for line in f if line.strip()]

pos = 50
min_pos = 0
max_pos = 99
end_on_zero_pos = 0
pass_zero_pos = 0

for line in lines:
    direction = line[0]
    steps = int(line[1:])
    
    for i in range(0, steps):
        if direction == 'L':
            pos -= 1
            if pos < min_pos:
                pos = max_pos
        elif direction == 'R':
            pos += 1
            if pos > max_pos:
                pos = min_pos
        if pos == min_pos:
            pass_zero_pos += 1

    if pos == min_pos:
        end_on_zero_pos += 1

print(f"Part 1 password is: {end_on_zero_pos}")
print(f"Part 2 password is: {pass_zero_pos}")