import os

def rename_files(folder_path):
    # List all files in the folder
    files = os.listdir(folder_path)
    jpg_files = [f for f in files if f.endswith(".jpg")]

    # Sort the files alphabetically
    jpg_files.sort()

    # Rename the files
    for index, file in enumerate(jpg_files, start=1):
        new_name = f"frame-{str(index).zfill(5)}.jpg"
        old_path = os.path.join(folder_path, file)
        new_path = os.path.join(folder_path, new_name)
        os.rename(old_path, new_path)
        print(f"Renaming: {file} -> {new_name}")

if __name__ == "__main__":
    folder_path = "D:/User/source/caktin_ws/YoloDatasets/236 B - Training/new dataset/CLASS _ Batang Pepaya -20230719T164722Z-001/CLASS _ Batang Pepaya"  # Replace this with the actual folder path
    rename_files(folder_path)
