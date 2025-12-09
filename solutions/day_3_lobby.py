import os

# Determine the project root directory
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Read input file
with open(os.path.join(root_dir, "inputs", "day_3_input.txt")) as f:
    lines = [line.strip() for line in f if line.strip()]

part_1_sum = 0
part_2_sum = 0

# Part 1 (selecting 2 batteries)
for line in lines:
    bank = list(map(int, line))

    # Let f[i] be the largest possible joltage achieved with battery bank[i] being selected as the second battery
    f = [-1 for i in range(0, len(bank))]
    f[1] = bank[0] + bank[1]

    # Let b[i] be the joltage level of the first battery chosen to achieve f[i] along with bank[i]
    b = [-1 for i in range(0, len(bank))]
    b[1] = bank[0]

    for i in range(2, len(bank)):
        case1 = f[i-1]                          # Case 1: f[i-1] is the highest possible pair
        case2 = 10*bank[i-1] + bank[i]          # Case 2: bank[i-1] and bank[i] is the highest possible pair
        case3 = 10*b[i-1] + bank[i]             # Case 3: b[i-1] and bank[i] is the highest possible pair
        f[i] = max(case1, case2, case3)

        if case1 == f[i]:
            b[i] = b[i-1]
        elif case2 == f[i]:
            b[i] = bank[i-1]
        else:
            b[i] = b[i-1]

    part_1_sum += max(f)

# Part 2 (selecting 12 batteries)
for line in lines:
    bank = list(map(int, line))
    n = len(bank)

    # Let f[i,j] be the joltage contribution of bank[i] when selected as digit j+1 (from left to right)
    f = [[-1 for j in range(0, 12)] for i in range(0, n)]
    for i in range(0, n):
        for j in range(0, 12):
            if j <= i and n-i >= 12-j:
                f[i][j] = pow(10, 12-j-1) * bank[i]

    # "Walk" f to compute the maximum possible joltage
    max_joltage = 0
    i_ptr = 0
    for j in range(0, 12):
        highest_contribution = -1
        i_highest = -1
        for i in range(i_ptr, n-12+j+1):
            if f[i][j] > highest_contribution:
                highest_contribution = f[i][j]
                i_highest = i
        max_joltage += highest_contribution
        i_ptr = i_highest + 1

    part_2_sum += max_joltage

# General case (covers both parts)
def compute_max_joltage(bank, n_digits):
    n = len(bank)

    # Let f[i,j] be the joltage contribution of bank[i] when selected as digit j+1 (from left to right)
    f = [[-1 for j in range(0, n_digits)] for i in range(0, n)]
    for i in range(0, n):
        for j in range(0, n_digits):
            if j <= i and n-i >= n_digits-j:
                f[i][j] = pow(10, n_digits-j-1) * bank[i]

    # "Walk" f to compute the maximum possible joltage
    max_joltage = 0
    i_ptr = 0
    for j in range(0, n_digits):
        highest_contribution = -1
        i_highest = -1
        for i in range(i_ptr, n-n_digits+j+1):
            if f[i][j] > highest_contribution:
                highest_contribution = f[i][j]
                i_highest = i
        max_joltage += highest_contribution
        i_ptr = i_highest + 1

    return max_joltage

part_1_sum_general = 0
part_2_sum_general = 0
for line in lines:
    bank = list(map(int, line))
    part_1_sum_general += compute_max_joltage(bank, 2)
    part_2_sum_general += compute_max_joltage(bank, 12)

print(f"Part 1 sum is: {part_1_sum}")     # Correct sum: 17766
print(f"Part 2 sum is: {part_2_sum}")     # Correct sum: 176582889354075

print(f"Part 1 sum (general case) is: {part_1_sum_general}")     # Correct sum: 17766
print(f"Part 2 sum (general case) is: {part_2_sum_general}")     # Correct sum: 176582889354075

if part_1_sum_general != part_1_sum:
    print("Part 1 sum (general case) is incorrect")
if part_2_sum_general != part_2_sum:
    print("Part 2 sum (general case) is incorrect")