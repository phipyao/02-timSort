for i in range(20):
    try:
        f = open(f"programmingChallenge/io/test.in.{i}", "x")
        f.close()
        print("File created successfully.")
    except FileExistsError:
        print("File already exists.")

for i in range(20):
    try:
        f = open(f"programmingChallenge/io/test.out.{i}", "x")
        f.close()
        print("File created successfully.")
    except FileExistsError:
        print("File already exists.")




for i in range(3):
    try:
        f = open(f"implementation/io/test.in.{i}", "x")
        f.close()
        print("File created successfully.")
    except FileExistsError:
        print("File already exists.")
    
for i in range(3):
    try:
        f = open(f"implementation/io/test.out.{i}", "x")
        f.close()
        print("File created successfully.")
    except FileExistsError:
        print("File already exists.")