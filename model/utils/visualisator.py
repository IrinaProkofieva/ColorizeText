import math
from PIL import Image
import spacy


# Соотношение класса-цвета и значения цвета в rgb
colors_rgb = {
    'БЕЛЫЙ': (255, 255, 255),
    'ЧЕРНЫЙ': (0, 0, 0),
    'СЕРЫЙ': (191, 191, 191),
    'КРАСНЫЙ': (252, 14, 3),
    'ОРАНЖЕВЫЙ': (251, 169, 35),
    'ЖЕЛТЫЙ': (248, 239, 37),
    'ЗЕЛЕНЫЙ': (52, 233, 12),
    'ГОЛУБОЙ': (12, 233, 226),
    'СИНИЙ': (13, 12, 233),
    'ФИОЛЕТОВЫЙ': (233, 12, 162),
    'КОРИЧНЕВЫЙ': (186, 73, 18)
}


# Функция для поиска двух самых близких друг к другу делителей числа
def nearestDivisors(n):
    divisors = (1, n)

    i = int(math.sqrt(n))
    while i >= 1:
        if (n % i == 0):
            if (n / i == i):
                return (i, i)
            else:
                return (i, int(n / i))
        i -= 1
    return divisors


# Функция для разбиения массива на массивы длиной n
def chunk(arr, n):
    return [arr[i:i + n] for i in range(0, len(arr), n)]


# Функция для повторения каждого элемента массива k раз:
# repeat([1, 2, 3], 2) -> [1, 1, 2, 2, 3, 3]
def repeat(arr, k):
    ans = []
    for el in arr:
        ans.extend([el] * k)
    return ans


# Функция для определения того, как будут располагаться цвета на изображении, для заполнения изображения цветом.
# Получает на вход последовательность встречаемых в тексте цветов и желаемый размер квадратного изображения, выдает
# массив значений пикселей на изобрадении и итоговый размер получившегося изображения
def resize(arr, size):
    # Определяем, сколько цветов в каждом ряду и сколько рядов будет на изображении
    # (два ближайших друг к другу делителя количества цветов в тексте)
    x = nearestDivisors(len(arr))
    x = tuple(sorted(x, reverse=True))
    # Делим цвета на ряды
    y = chunk(arr, x[0])
    # Определяем размер итогового изображения
    w = (size // len(y[0])) * len(y[0])
    h = (size // len(y)) * len(y)

    ans = []
    for row in y:
        # Заполняем цветами ряд (заполнение по горизонтали)
        longRow = repeat(row, size // len(y[0]))
        # Заполняем рядами - сколько раз ряд повторяется (заполнение по горизонтали)
        longRow = longRow * (size // len(y))
        ans.extend(longRow)
    return ans, w, h


# Итоговая функция визуализации
def visualize(doc, size):
    # Получаем именнованные сущности в тексте
    ents_parse = spacy.displacy.parse_ents(doc)
    # Преобразуем названия цветов в значения RGB
    colors = [colors_rgb[x['label']] for x in ents_parse['ents']]
    # Получаем массив значений пикселей
    img_bytes, w, h = resize(colors, size)
    # формируем изображение
    img = Image.new('RGB', (w, h))
    img.putdata(img_bytes)
    return img
