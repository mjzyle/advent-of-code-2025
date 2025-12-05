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

    # Note if we are starting from the minimum position
    starting_from_zero_pos = pos == min_pos

    # Determine number of full rotations
    full_rotations = steps // (max_pos - min_pos + 1)
    remaining_steps = steps % (max_pos - min_pos + 1)

    # For each full rotation, we pass the minimum position exactly once
    pass_zero_pos += full_rotations

    # Determine overage amount if remaining steps roll past the min or max position
    overage = 0
    if direction == 'L' and remaining_steps > pos - min_pos:
        overage = remaining_steps - (pos - min_pos)
    elif direction == 'R' and remaining_steps + pos > max_pos:
        overage = remaining_steps + pos - max_pos

    # Set final position
    if direction == 'L':
        pos = pos - remaining_steps if overage == 0 else max_pos - overage + 1
    elif direction == 'R':
        pos = pos + remaining_steps if overage == 0 else min_pos + overage - 1

    # Determine if applying the remaining steps results in a pass through the minimum position
    if overage > 0 and not starting_from_zero_pos:
        pass_zero_pos += 1

    # Count cases where we end at zero but didn't start from zero
    if not starting_from_zero_pos and pos == min_pos and overage == 0:
        pass_zero_pos += 1

    if pos == min_pos:
        end_on_zero_pos += 1

print(f"Part 1 password is: {end_on_zero_pos}")     # Correct password: 1097
print(f"Part 2 password is: {pass_zero_pos}")       # Correct password: 7101