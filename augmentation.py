import Augmentor
from PIL import Image
import random
import os
import numpy as np

# Кручу верчу
# data = Augmentor.Pipeline('target_camouflage')
#
# data.rotate(probability=0.7, max_left_rotation=5, max_right_rotation=5)
# data.skew_left_right(probability=0.7, magnitude=0.3)
# data.skew_top_bottom(probability=0.7, magnitude=0.3)
#
# data.process()


# Пошумим немного

def add_noise_to_image(input_folder, output_folder):

    # Проверяем, что папка назначения существует
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Получаем список файлов в папке с изображениями
    image_files = [f for f in os.listdir(input_folder) if f.endswith('.png')]

    for image_file in image_files:
        input_path = os.path.join(input_folder, image_file)
        output_path = os.path.join(output_folder, image_file)

        # Открываем изображение
        image = Image.open(input_path)

        # Преобразуем изображение в массив NumPy для более быстрой обработки
        pixels = np.array(image)

        # Генерируем шум для каждого канала цвета (RGB)
        noise_intensity = random.randint(3, 8) * 10

        noise = np.random.randint(-noise_intensity, noise_intensity + 1, size=pixels.shape, dtype=np.int16)

        # Добавляем шум к пикселям
        noisy_pixels = np.clip(pixels + noise, 0, 255).astype(np.uint8)

        # Создаем новое изображение из массива NumPy
        noisy_image = Image.fromarray(noisy_pixels)

        # Сохраняем изображение с новым шумом в папку назначения
        noisy_image.save(output_path)


input_folder = "C:\\Users\\KFU\\Desktop\\Biathlon-M\\data_preparation\\target_camouflage"
output_folder = "C:\\Users\\KFU\\Desktop\\Biathlon-M\\data_preparation\\augmented_target"


add_noise_to_image(input_folder, output_folder)