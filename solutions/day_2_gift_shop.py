import os

# Determine the project root directory
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Read input file
with open(os.path.join(root_dir, "inputs", "day_2_input.txt")) as f:
    lines = [line.strip() for line in f if line.strip()]

# O(n) because there should be only one line; n is the number of ranges
ranges = []
for line in lines:
    ranges_str =line.split(',')
    for r in ranges_str:
        ranges.append(list(map(int, r.split('-'))))

part_1_sum = 0
part_2_sum = 0
for r in ranges:
    for i in range(r[0], r[1]+1):
        i_str = str(i)
        divisor = 2
        len_pattern = len(i_str) // divisor
        while len_pattern > 0:
            # Part 1: Check if the number is a repeating pattern of length 2
            if divisor == 2:
                if i_str[:len_pattern] == i_str[len_pattern:]:
                    part_1_sum += i
                    part_2_sum += i
                    break
            # Part 2: Check if the number is a repeating pattern of any length
            else:
                pattern = i_str[:len_pattern]
                if i_str.replace(pattern, '') == '':
                    part_2_sum += i
                    break
            divisor += 1
            len_pattern = len(i_str) // divisor
        
print(f"Part 1 sum is: {part_1_sum}")     # Correct sum: 18700015741
print(f"Part 2 sum is: {part_2_sum}")     # Correct sum: 20077272987