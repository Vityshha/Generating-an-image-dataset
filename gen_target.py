from PIL import Image
import os


def apply_texture(image, texture, mask):
    textured_image = Image.new('RGBA', image.size)

    for y in range(image.size[1]):
        for x in range(image.size[0]):
            if mask.getpixel((x, y)) == 255:
                texture_pixel = texture.getpixel((x, y))
                textured_image.putpixel((x, y), texture_pixel)
            else:
                image_pixel = image.getpixel((x, y))
                textured_image.putpixel((x, y), image_pixel)

    return textured_image

def recolor_image(image_path, texture_path, output_folder, idx):
    try:
        # Открываем изображение мишени
        image = Image.open(image_path)

        # Открываем текстуру с альфа-каналом
        texture = Image.open(texture_path)

        # Размеры изображения мишени
        width, height = image.size

        # Масштабируем текстуру до размеров изображения мишени
        texture = texture.resize((width, height))

        # Получаем маску объекта на исходном изображении
        mask = image.convert('L').point(lambda x: 255 if x < 240 else 0, mode='1')

        # Применяем текстуру с учетом маски объекта
        textured_image = apply_texture(image, texture, mask)

        # Получаем имя файла без расширения
        file_name = os.path.splitext(os.path.basename(image_path))[0]

        # Создаем новый путь сохранения с суффиксом "_camouflage"
        output_path = os.path.join(output_folder, f"{file_name}"+str(idx)+".png")

        # Сохраняем изображение с текстурой
        textured_image.save(output_path)
        print(f"Применена текстура к изображению: {output_path}")
    except Exception as e:
        print(f"Ошибка при обработке изображения {image_path}: {e}")


def main():
    # Укажите путь к папке с изображениями мишеней
    folder_path = "target"

    # Укажите путь к папке с текстурами
    textures_folder = "textures"

    # Укажите путь к папке для сохранения изображений с текстурами
    output_folder = "target_camouflage"

    # Создаем папку для сохранения изображений с текстурами, если она не существует
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Получаем список всех файлов в папке с текстурами
    texture_files = os.listdir(textures_folder)

    # Фильтруем файлы, оставляя только png текстуры
    texture_files = [f for f in texture_files if f.lower().endswith('.png')]

    # Получаем список всех файлов в папке с изображениями мишеней
    file_list = os.listdir(folder_path)

    # Фильтруем файлы, оставляя только png изображения
    png_files = [f for f in file_list if f.lower().endswith('.png')]

    # Применяем текстуры к каждому изображению
    for png_file in png_files:
        image_path = os.path.join(folder_path, png_file)

        for idx, texture_file in enumerate(texture_files):
            texture_path = os.path.join(textures_folder, texture_file)
            recolor_image(image_path, texture_path, output_folder, idx)


if __name__ == "__main__":
    main()
