import os

def rename_files(folder_path, target_extension='.mp4', output_prefix='video-'):
    if not os.path.exists(folder_path):
        print(f"Folder '{folder_path}' tidak ditemukan.")
        return

    file_list = os.listdir(folder_path)
    video_files = [file for file in file_list if file.lower().endswith(target_extension)]
    video_files.sort()

    if not video_files:
        print(f"Tidak ditemukan file dengan ekstensi '{target_extension}' di folder '{folder_path}'.")
        return

    count = 1
    for file in video_files:
        old_path = os.path.join(folder_path, file)
        new_name = f"{output_prefix}{count}{target_extension}"
        new_path = os.path.join(folder_path, new_name)
        os.rename(old_path, new_path)
        print(f"File '{file}' berhasil diubah menjadi '{new_name}'.")
        count += 1

if __name__ == "__main__":
    folder_path = input("Masukkan alamat folder yang ingin diubah: ")
    rename_files(folder_path)
