
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
# pypy3 pcSol_python.py < ../io/test.in.20 > ../io/test.out.20
filename = f"programmingChallenge/io/test.in.{20}"

# Write to the file
with open(filename, "w") as f:

    n = 300000
    q = 10
    f.write(f"{n} {q}\n")
    
    points = []
    for i in range(n):
        x = random.randint(-1000, 1000)
        y = random.randint(-1000, 1000)
        points.append((x, y))
    
    # points.sort(key=lambda p: (polar_angle(p), distance_squared(p)))
    # points = points[::-1]

    for i in range(n):
        f.write(f"{points[i][0]} {points[i][1]} {i+1}\n")

    for i in range(q):
        r = random.randint(5, 150)
        f.write(f"{r}\n")

# Read from the file and print contents
with open(filename, "r") as f:
    print(f.read())
