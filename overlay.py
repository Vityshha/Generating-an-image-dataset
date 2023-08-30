from PIL import Image, ImageFilter, ImageDraw, ImageFile
import os
import random
import numpy as np
from tqdm import tqdm

def overlay_images(background_path, overlay_path, output_folder, j):

    ImageFile.LOAD_TRUNCATED_IMAGES = True
    background = Image.open(background_path)
    overlay = Image.open(overlay_path)

    # Перевод в формат yolo 640 на 640
    background = background.resize((640, 640))

    # Список коэффициентов масштабирования
    scale_factors = [0.16, 0.13, 0.1]


    for scale_factor in scale_factors:
        # Масштабируем изображение из target_camouflage
        scaled_overlay = overlay.resize((int(overlay.size[0] * scale_factor), int(overlay.size[1] * scale_factor)))

        result = background.copy()

        # Случайное наложение шумов и размытия фона
        i = random.randint(1, 15)
        if i == 1:
            result = result.filter(ImageFilter.BLUR)
        elif i == 2:
            result = result.filter(ImageFilter.MinFilter(3))


        k = random.randint(1, 8)
        if k == 1:
            pixels = np.array(result)
            noise_intensity = random.randint(3, 8) * 10
            noise = np.random.randint(-noise_intensity, noise_intensity + 1, size=pixels.shape, dtype=np.int16)
            noisy_pixels = np.clip(pixels + noise, 0, 255).astype(np.uint8)
            result = Image.fromarray(noisy_pixels)

        # Вычисляем случайные координаты для наложения изображения
        x = random.randint(0, background.size[0] - scaled_overlay.size[0])
        y = random.randint(0, background.size[1] - scaled_overlay.size[1])

        # print('КООРДИНАТЫ X, Y: ', x, y)
        # print('НОВАЯ Y: ', y + scaled_overlay.height)
        # print('НОВЫЙ X :', x + scaled_overlay.width)

        box = str(0) + ' ' + str(x/640) + ' ' + str(y/640) + ' ' + str((scaled_overlay.width)/640) + ' ' + str((scaled_overlay.height)/640)

        # Наложение изображение на фон
        result.paste(scaled_overlay, (x, y), scaled_overlay)


        # Проверка координат
        # img1 = ImageDraw.Draw(result)
        # shape=[(x, y), (x+scaled_overlay.width, y+scaled_overlay.height)]
        # img1.rectangle(shape, fill=None, outline="red")

        # Сохраняем результат с уникальным именем
        filename, ext = os.path.splitext(os.path.basename(overlay_path))

        output_path_img = os.path.join(output_folder+'/image', f"{filename}_{j}.jpg")
        output_path_label = os.path.join(output_folder + '/label', f"{filename}_{j}.txt")

        result.save(output_path_img)

        file = open(output_path_label, 'w')
        file.write(box)
        file.close()

def main():
    backgrounds_folder = "backgrounds_folder"
    target_camouflage = "augmented_target"
    output_folder = "ready"


    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    j = 0

    # Перебираем фоны и мишени
    for background_file in tqdm(os.listdir(backgrounds_folder)):
        background_path = os.path.join(backgrounds_folder, background_file)
        for overlay_file in os.listdir(target_camouflage):
            overlay_path = os.path.join(target_camouflage, overlay_file)
            try:
                overlay_images(background_path, overlay_path, output_folder, j)
            except:
                print('Error')
            j += 1


if __name__ == "__main__":
    main()
