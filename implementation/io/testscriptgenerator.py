for i in range(20):
    try:
        f = open(f"test.in.{i}", "x")
        f.close()
        print("File created successfully.")
    except FileExistsError:
        print("File already exists.")

for i in range(20):
    try:
        f = open(f"test.out.{i}", "x")
        f.close()
        print("File created successfully.")
    except FileExistsError:
        print("File already exists.")
