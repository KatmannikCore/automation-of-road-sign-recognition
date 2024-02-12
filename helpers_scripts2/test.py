from PIL import Image
import pytesseract

# Укажите путь к исполняемому файлу tesseract.exe
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\Urbanovich\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'

# Укажите путь к изображению, с которого нужно считать текст
image_path = r'D:\Urban\yolov4\yolov4-opencv-python\train\54\0_1.0%.jpg'

# Открываем изображение
img = Image.open(image_path)

# Используем pytesseract для извлечения текста с изображения
text = pytesseract.image_to_string(img, lang='rus')

print(text)

import easyocr

# Инициализация ридера
reader = easyocr.Reader(['ru'])  # Укажите язык или языки, которые вы хотите распознавать

# Чтение текста с изображения
result = reader.readtext(image_path)

# Вывод результатов
for (bbox, text, prob) in result:
    print(f'Текст: {text} (Вероятность: {prob:.2f})')