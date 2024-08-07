from PIL import Image
import os

def resize_images(input_dir, output_dir, width, height):
    """Изменяет размер всех изображений в указанной папке.

    Args:
        input_dir (str): Путь к папке с изображениями.
        output_dir (str): Путь к папке для сохранения измененных изображений.
        width (int): Новая ширина изображения.
        height (int): Новая высота изображения.
    """

    for filename in os.listdir(input_dir):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            # Открываем изображение
            img = Image.open(os.path.join(input_dir, filename))

            # Изменяем размер изображения
            img = img.resize((width, height))

            # Сохраняем измененное изображение
            img.save(os.path.join(output_dir, filename))

# Пример использования:
input_dir = rf"D:\Urban\map\24\ffffff"  # Замените на путь к папке с изображениями
output_dir = rf"D:\Urban\map\100"  # Замените на путь к папке для сохранения
width = 100  # Задайте желаемую ширину
height = 100  # Задайте желаемую высоту

resize_images(input_dir, output_dir, width, height)
print("Изменение размера изображений завершено!")
