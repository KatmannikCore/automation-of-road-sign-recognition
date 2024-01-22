
import potrace
from PIL import Image

# Открываем изображение в формате JPG
image = Image.open('image.jpg')

# Преобразуем изображение в черно-белый формат
image = image.convert('1')

# Создаем объект Potrace
p = potrace.p()

# Преобразуем изображение в формат SVG
svg = p.trace(image)

# Сохраняем SVG-файл
with open('image.svg', 'w') as f:
    f.write(svg)
from svgpathtools import svg2paths, Path, Line

# Загрузка SVG файла
paths, attributes = svg2paths('image.svg')

# Извлечение контуров и их свойств
for path in paths:
    length = path.length()
    center = path.center()
    area = path.area()
    print(f"Длина: {length}, Центр: {center}, Площадь: {area}")

# Создание нового контура
line = Line(0+0j, 100+100j)
path = Path(line)
path.stroke_width = 2
path.stroke = 'black'

print(path)
# Экспорт контура в SVG файл
path.write_svg('line.svg')

# Загрузка SVG файла
#paths, attributes = svg2paths('./contours.svg')

#print(paths, attributes)
# Load image
#img = cv2.imread('./248.svg')
#print(img)
## Convert to grayscale
#gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#
## Apply threshold filter
#ret, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
#
## Apply morphological closing
#kernel = np.ones((5,5),np.uint8)
#closing = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
#
## Find contours
#contours, hierarchy = cv2.findContours(closing, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
#
## Filter contours
#for cnt in contours:
#    approx = cv2.approxPolyDP(cnt, 0.01*cv2.arcLength(cnt,True),True)
#    if len(approx) == 7:
#        cv2.drawContours(img, [cnt], 0, (0,0,255), 2)
#
## Display image
#cv2.imshow('image', img)
#cv2.waitKey(0)
#cv2.destroyAllWindows()