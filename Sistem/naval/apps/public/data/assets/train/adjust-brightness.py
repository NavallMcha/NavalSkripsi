from PIL import Image, ImageEnhance
import os

def adjust_brightness(image_path, brightness_factor):
    img = Image.open(image_path)
    enhancer = ImageEnhance.Brightness(img)
    bright_img = enhancer.enhance(brightness_factor)
    return bright_img

def rename_files(folder_path):
    image_files = [f for f in os.listdir(folder_path) if f.endswith('.jpg')]

    for image_file in image_files:
        image_path = os.path.join(folder_path, image_file)
        label_path = os.path.join(folder_path, image_file.replace('.jpg', '.txt'))

        # Menurunkan brightness gambar dengan faktor 0.5 (nilai < 1 mengurangi kecerahan)
        bright_img = adjust_brightness(image_path, 1.5)

        # Simpan gambar yang sudah diberi efek penurunan brightness
        new_image_path = image_path.replace('.jpg', '_hi.jpg')
        bright_img.save(new_image_path)

        # Ubah nama label file sesuai dengan gambar yang sudah diubah namanya
        new_label_path = label_path.replace('.txt', '_hi.txt')
        os.rename(label_path, new_label_path)

        # Hapus file gambar dan label yang lama
        os.remove(image_path)
        # os.remove(label_path)
        print(image_path)

if __name__ == "__main__":
    folder_path = "D:/User/source/caktin_ws/YoloDatasets/236 B - Training/grape-datasets-new-sidang/grape-new-S - Copy (2)"  # Ganti dengan path folder yang sesuai
    rename_files(folder_path)
