import os
import random
import shutil

# Путь к исходной папке с файлами
source_folder_image = "C:\\Users\\KFU\\Desktop\\Biathlon-M\\data_preparation\\ready\\image"
source_folder_label = "C:\\Users\\KFU\\Desktop\\Biathlon-M\\data_preparation\\ready\\label"

# Пути к новым папкам для train, test и valid
train_images = "C:\\Users\\KFU\\Desktop\\Biathlon-M\\yolo-train\\train\\image"
train_label = "C:\\Users\\KFU\\Desktop\\Biathlon-M\\yolo-train\\train\\label"

valid_images = "C:\\Users\\KFU\\Desktop\\Biathlon-M\\yolo-train\\valid\\image"
valid_label = "C:\\Users\\KFU\\Desktop\\Biathlon-M\\yolo-train\\valid\\label"

test_images = "C:\\Users\\KFU\\Desktop\\Biathlon-M\\yolo-train\\test\\image"
test_label = "C:\\Users\\KFU\\Desktop\\Biathlon-M\\yolo-train\\test\\label"

# Создание новых папок, если они еще не существуют
os.makedirs(train_images, exist_ok=True)
os.makedirs(train_label, exist_ok=True)
os.makedirs(valid_images, exist_ok=True)
os.makedirs(valid_label, exist_ok=True)
os.makedirs(test_images, exist_ok=True)
os.makedirs(test_label, exist_ok=True)

# Проход по всем файлам в исходной папке
for file_image in os.listdir(source_folder_image):
    # Полный путь к файлу
    file_path_im = os.path.join(source_folder_image, file_image)
    file_label = file_image[:-4] + '.txt'
    file_path_lb = os.path.join(source_folder_label, file_label)

    # Определение папки, в которую нужно переместить файл
    folder_im = ""
    folder_lb = ""
    rand = random.random()  # случайное число от 0 до 1

    if rand < 0.70:
        folder_im = train_images
        folder_lb = train_label
    elif 0.70 <= rand < 0.85:
        folder_im = valid_images
        folder_lb = valid_label
    else:
        folder_im = test_images
        folder_lb = test_label

    # Перемещение файла
    shutil.move(file_path_im, folder_im)
    shutil.move(file_path_lb, folder_lb)