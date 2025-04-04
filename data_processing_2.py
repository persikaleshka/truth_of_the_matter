import pandas as pd
import re

df = pd.read_csv("unprocessed_data_all.csv")  


df["region_id"] = df["region"]
region_counts = df["region_id"].value_counts().sort_values(ascending=False)
region_counts.to_csv("region_stats_by_id_all.csv")

def clean_text(text):
    text = re.sub(r"http[s]?://\S+", "", str(text))  
    text = re.sub(r"<адрес>", "[ADDRESS]", text)
    text = re.sub(r"<данные изъяты>", "[REDACTED]", text)
    text = re.sub(r"[-;]+", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

def extract_entities(text):
    entities = []
    patterns = [
        (r"\b[А-ЯЁ][а-яё]+(?:-[А-ЯЁа-яё]+)?\s[А-ЯЁ]\.[А-ЯЁ]\.", "B-PER"),  
        (r"\b(?:ст\.?|стать[яеи]|статьей|по\sстать[еий]|статьи)\s?\d+(?:\.\d+)?(?:\s?ч\.?\s?\d+)?\b|"
         r"\bч\.?\s?\d+\sст\.?\s?\d+(?:\.\d+)?\b|"
         r"\bчаст[ьи]\s\d+\sстать[ией]\s\d+(?:\.\d+)?\b", "B-LAW"),
        (r"(?:\d{1,2}[\. ]\d{1,2}[\. ]\d{4}(?:\s?г(?:\.|ода)?\.?)?|"
         r"\d{1,2}\s?(?:январ[ьяеюем]|феврал[ьяеюем]|март[аеуом]?|"
         r"апрел[ьяеюем]|ма[яеюем]|июн[ьяеюем]|июл[ьяеюем]|август[аеуом]?|"
         r"сентябр[ьяеюем]|октябр[ьяеюем]|ноябр[ьяеюем]|декабр[ьяеюем])"
         r"\s?\d{4}(?:\s?г(?:\.|ода)?\.?)?|"
         r"(?:в\s)?(?:январ[ьяеюем]|феврал[ьяеюем]|март[аеуом]?|"
         r"апрел[ьяеюем]|ма[яеюем]|июн[ьяеюем]|июл[ьяеюем]|август[аеуом]?|"
         r"сентябр[ьяеюем]|октябр[ьяеюем]|ноябр[ьяеюем]|декабр[ьяеюем])"
         r"\s\d{4}(?:\s?г(?:\.|ода)?\.?)?)", "B-DATE"),
        (r"\b\d{1,3}(?:[\s\u00A0]?\d{3})*(?:[.,]\d{1,2})?"
         r"(?:\s?(?:тыс|млн))?"
         r"\s?(?:руб(?:\.|лей|ль)?|р\.)"
         r"(?:\s\d{1,2}\s?коп(?:\.|еек)?)?","B-MONEY"),
        (r"\b(?:Республика\s[А-ЯЁа-яё]+|Республики\s[А-ЯЁа-яё]+|"
         r"[А-ЯЁа-яё]+ская\sобласть|[А-ЯЁа-яё]+ской\sобласти|"
         r"[А-ЯЁа-яё]+ский\sкрай|[А-ЯЁа-яё]+ского\sкрая|"
         r"(?:г\.\s?|города\s|город\s|г\s?)?(?:Москв[а-яё]*|Санкт[-\s]?Петербург[а-яё]*))\b", "B-REGION")
    ]
    for pattern, label in patterns:
        for match in re.finditer(pattern, text):
            entities.append({"start": match.start(), "end": match.end(), "label": label})
    return entities


df = df[df["text"].notna()]
df = df[df["text"].str.strip() != ""]
df = df[df["text"] != "-"]

df["text"] = df["text"].apply(clean_text)
df["entities"] = df["text"].apply(extract_entities)

region_counts = df["region_id"].value_counts().sort_values(ascending=False)
region_counts.to_csv("region_stats_by_id_with_text.csv")

df = df.sort_values(by="region_id")
df_for_model = df[["region_id", "text"]]
df_for_model.to_csv("processed_data_penalty.csv", index=False)

columns_to_drop = [
    "id", "region", "instance", "court_name", "caseNumber", "entryDate", "names", 
    "judge", "resultDate", "decision", "endDate", "consideredBy", "cui", 
    "link_meta", "link_text", "link_text_and_meta", "connected_links_1", 
    "connected_links_2", "connected_links_3", "connected_links_4", "region_id"
]
df = df.drop(columns=columns_to_drop, errors="ignore")

df["text"] = df["text"].str.replace('"', "'")
df.to_csv("processed_data_all.csv", index=False)
