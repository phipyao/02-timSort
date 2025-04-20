
# for i in range(3):
#     try:
#         f = open(f"implementation/io/test.in.{i+1}", "x")
#         f.close()
#         print("File created successfully.")
#     except FileExistsError:
#         print("File already exists.")
    
# for i in range(3):
#     try:
#         f = open(f"implementation/io/test.out.{i+1}", "x")
#         f.close()
#         print("File created successfully.")
#     except FileExistsError:
#         print("File already exists.")

# for i in range(20):
#     try:
#         f = open(f"programmingChallenge/io/test.in.{i+1}", "x")
#         f.close()
#         print("File created successfully.")
#     except FileExistsError:
#         print("File already exists.")

# for i in range(20):
#     try:
#         f = open(f"programmingChallenge/io/test.out.{i+1}", "x")
#         f.close()
#         print("File created successfully.")
#     except FileExistsError:
#         print("File already exists.")

import random
import math

def polar_angle(p):
    x, y = p
    return math.atan2(-y, -x)

def distance_squared(p):
    x, y = p
    return x * x + y * y

# Define the file path
# python3 pcSol_python.py < ../io/test.in.9 > ../io/test.out.9 && cat ../io/test.out.9
filename = f"programmingChallenge/io/test.in.{9}"

# Write to the file
with open(filename, "w") as f:
    points = []
    for i in range(20):
        x = random.randint(-20, 20)
        y = random.randint(-20, 20)
        points.append((x, 0))
    
    f.write("20 1\n")

    # points.sort(key=lambda p: (polar_angle(p), distance_squared(p)))
    # points = points[::-1]

    for i in range(20):
        f.write(f"{points[i][0]} {points[i][1]} {i+1}\n")

    f.write("40")

# Read from the file and print contents
with open(filename, "r") as f:
    print(f.read())
