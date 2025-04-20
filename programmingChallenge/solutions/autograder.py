import subprocess

def run_command(command):
    """Executes a terminal command and returns the result."""
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    return stdout.decode(), stderr.decode()

def main():
    # Define the file paths
    input_file = "../io/test.in.1"
    expected_output = "../io/test.out.1"
    
    # Command 1: C++ (g++)
    print("Running C++ code...")
    command_cpp = "g++ -std=c++17 -o timsort pcSol_cpp.cpp && ./timsort < {} > output".format(input_file)
    stdout, stderr = run_command(command_cpp)
    if stderr:
        print(f"C++ compilation or execution error: {stderr}")
    else:
        print("C++ output generated.")
        command_diff = "diff output {}".format(expected_output)
        diff_stdout, diff_stderr = run_command(command_diff)
        if diff_stderr:
            print(f"Error during diff (C++): {diff_stderr}")
        elif diff_stdout:
            print(f"Differences (C++):\n{diff_stdout}")
        else:
            print("C++ output matches expected output.")

    # Command 2: Java
    print("\nCompiling Java code...")
    command_compile_java = "javac pcSol_java.java"
    stdout, stderr = run_command(command_compile_java)
    if stderr:
        print(f"Java compilation error: {stderr}")
    else:
        print("Java compiled successfully.")

    print("\nRunning Java code...")
    command_java = "java pcSol_java < {} > output".format(input_file)
    stdout, stderr = run_command(command_java)
    if stderr:
        print(f"Java execution error: {stderr}")
    else:
        print("Java output generated.")
        command_diff = "diff output {}".format(expected_output)
        diff_stdout, diff_stderr = run_command(command_diff)
        if diff_stderr:
            print(f"Error during diff (Java): {diff_stderr}")
        elif diff_stdout:
            print(f"Differences (Java):\n{diff_stdout}")
        else:
            print("Java output matches expected output.")

    # Command 3: Python
    print("\nRunning Python code...")
    command_python = "python3 pcSol_python.py < {} > output".format(input_file)
    stdout, stderr = run_command(command_python)
    if stderr:
        print(f"Python execution error: {stderr}")
    else:
        print("Python output generated.")
        command_diff = "diff output {}".format(expected_output)
        diff_stdout, diff_stderr = run_command(command_diff)
        if diff_stderr:
            print(f"Error during diff (Python): {diff_stderr}")
        elif diff_stdout:
            print(f"Differences (Python):\n{diff_stdout}")
        else:
            print("Python output matches expected output.")

if __name__ == "__main__":
    main()
