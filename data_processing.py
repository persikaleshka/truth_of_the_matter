import pandas as pd
import re

df = pd.read_csv("unprocessed_data.csv", delimiter=";")  

# Шаг 2: Функция для очистки текста
def clean_text(text):
    text = re.sub(r"http[s]?://\S+", "", str(text))  # Удаление ссылок
    text = re.sub(r"<адрес>", "[ADDRESS]", text)  # Заменяем адреса
    text = re.sub(r"<данные изъяты>", "[REDACTED]", text)  # Анонимизированные данные
    text = re.sub(r"[-;]+", " ", text)  # Удаление лишних пунктуаций
    text = re.sub(r"\s+", " ", text).strip()  # Удаление лишних пробелов
    return text


# Шаг 3: Функция для выделения сущностей
def extract_entities(text):
    entities = []
    patterns = [
        (r"\b[А-ЯЁ][а-яё]+\s[А-ЯЁ]\.\s?[А-ЯЁ]\.\b", "B-PER"),  # Имена
        (r"\bст\.\d+\sч\.\d+\b", "B-LAW"),                   # Статьи УК
        (r"\b\d{2}\s[а-я]+\s\d{4}\b", "B-DATE")             # Даты
    ]
    for pattern, label in patterns:
        for match in re.finditer(pattern, text):
            entities.append({"start": match.start(), "end": match.end(), "label": label})
    return entities

columns_to_drop = [
    "id", "region", "instance", "court_name", "caseNumber", "entryDate", "names", 
    "judge", "resultDate", "decision", "endDate", "consideredBy", "cui", 
    "link_meta", "link_text", "link_text_and_meta", "connected_links_1", 
    "connected_links_2", "connected_links_3", "connected_links_4"
]
df = df[df["text"] != "-"]
df = df.drop(columns=columns_to_drop, errors="ignore")

# Шаг 4: Очистить текст и выделить сущности
df["text"] = df["text"].apply(clean_text)  # Очистка текста
df["entities"] = df["text"].apply(extract_entities)  # Выделение сущностей

# Шаг 5: Сохранить результат в новый CSV-файл
df.to_csv("processed_data.csv", index=False)
