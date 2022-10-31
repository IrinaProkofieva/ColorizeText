import tqdm
import spacy
from spacy.tokens import DocBin
import json


# Метод для перевода датасета из json в spacy формат
def convert_to_spacy(data, save_path):
    # NLP объект для русского языка
    nlp = spacy.blank("ru")
    # Объект для хранения сериализованных размеченных текстов
    db = DocBin()
    # Для каждого текста из датасета
    for text, annot in tqdm(data['annotations']):
        # Создаем документ из текста
        doc = nlp.make_doc(text)
        ents = []
        # Для каждого размеченного объекта в тексте
        for start, end, label in annot['entities']:
            # Переводим в формат разметок spacy
            span = doc.char_span(start, end, label=label)
            if span is None:
                print("Skipping entity")
            else:
                ents.append(span)
        doc.ents = ents
        db.add(doc)

    # Сохраняем полученный датасет
    db.to_disk(save_path)


# Подготавливаем данные
def prepare_data():
    # Тренировочные данные
    f = open('../../annotations_train.json')
    train_data = json.load(f)
    convert_to_spacy(train_data, '../training_data.spacy')
    # Валидационные данные
    f = open('../../annotations_val.json')
    val_data = json.load(f)
    convert_to_spacy(val_data, '../val_data.spacy')
