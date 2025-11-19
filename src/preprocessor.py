def read_logs(file_path):
    with open(file_path, 'r') as f:
        logs = f.readlines()
    return logs

if __name__ == "__main__":
    logs = read_logs("../data/sample_logs.txt")
    print("Raw log lines:")
    for line in logs:
        print(line.strip())
# It ONLY reads the logs and prints them.

