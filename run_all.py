import os

base = "test_data"

for folder in os.listdir(base):

    folder_path = os.path.join(base, folder)

    # skip non-directories
    if not os.path.isdir(folder_path):
        continue

    json_file = f"{folder_path}/{folder}.json"
    output_file = f"output/{folder}.json"

    if os.path.exists(json_file):
        os.system(f"python3 test.py {json_file} {output_file}")

print("All files processed")
