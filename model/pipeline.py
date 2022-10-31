import spacy
import sys
from utils import visualisator


# Основной сценарий работы с текстом (текст передается через имя файла)
def pipeline(model, filename):
    with open(filename, mode="r", encoding="utf-8") as f:
        text = f.read()
        # Модель анализирует текст, выделяем цвета и выдает документ
        doc = model(text)
        # Визуализируем
        img = visualisator.visualize(doc, 255)
        # Сохраняем полученное изображение
        img.save("result.png")


nlp_ner = spacy.load('best-model')
filepath = sys.argv[1]
pipeline(nlp_ner, filepath)
