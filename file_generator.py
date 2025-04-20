
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

# Define the file path
filename = f"programmingChallenge/io/test.in.{4}"

# Write to the file
with open(filename, "w") as f:
    f.write("300\n")
    for i in range(300):
        random_int = random.randint(1, 1000)
        f.write(f"{random_int}\n")

# Read from the file and print contents
with open(filename, "r") as f:
    print(f.read())
