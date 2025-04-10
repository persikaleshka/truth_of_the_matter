import pandas as pd
import re

df = pd.read_csv("processed_data_penalty.csv")

fine_pattern = re.compile(
    r"""
    (?:назнач(?:ен|ается|ить)\s+)?          
    штраф(?:[ауом]{0,2})?                   
    (?:\s*(?:в\s+размере|на\s+сумму))?      
    \s*
    (\d{1,3}(?:[\s\u00A0]?\d{3})*|\d+(?:[.,]\d+)?)   
    \s*
    (тыс(\.)?|млн(\.)?)?                              
    \s*
    (?:руб(?:\.|лей|ль)?|р\.)               
    """,
    flags=re.IGNORECASE | re.VERBOSE
)

def extract_fines(text):
    fines = []
    for match in fine_pattern.finditer(text):
        amount_str = match.group(1).replace(" ", "").replace("\u00A0", "").replace(",", ".")
        multiplier = match.group(2)
        try:
            amount = float(amount_str)
            if multiplier == "тыс":
                amount *= 1_000
            elif multiplier == "млн":
                amount *= 1_000_000
            fines.append(int(amount))
        except ValueError:
            continue
    return [max(fines)] if fines else []

df["fine_amounts"] = df["text"].apply(extract_fines)

df_fines = df.explode("fine_amounts").dropna(subset=["fine_amounts"])
df_fines["fine_amounts"] = df_fines["fine_amounts"].astype(int)

fine_stats = df_fines.groupby("region_id")["fine_amounts"].agg(
    count="count",
    mean="mean",
    median="median",
    max="max"
).reset_index()

region_mapping = {
    1: "Республика Адыгея",
    2: "Республика Башкортостан",
    3: "Республика Бурятия",
    4: "Республика Алтай",
    5: "Республика Дагестан",
    6: "Республика Ингушетия",
    7: "Кабардино-Балкарская Республика",
    8: "Республика Калмыкия",
    9: "Карачаево-Черкесская Республика",
    10: "Республика Карелия",
    11: "Республика Коми",
    12: "Республика Марий Эл",
    13: "Республика Мордовия",
    14: "Республика Саха (Якутия)",
    15: "Республика Северная Осетия — Алания",
    16: "Республика Татарстан",
    17: "Республика Тыва",
    18: "Удмуртская Республика",
    19: "Республика Хакасия",
    20: "Чеченская Республика",
    21: "Чувашская Республика",
    22: "Алтайский край",
    23: "Краснодарский край",
    24: "Красноярский край",
    25: "Приморский край",
    26: "Ставропольский край",
    27: "Хабаровский край",
    28: "Амурская область",
    29: "Архангельская область",
    30: "Астраханская область",
    31: "Белгородская область",
    32: "Брянская область",
    33: "Владимирская область",
    34: "Волгоградская область",
    35: "Вологодская область",
    36: "Воронежская область",
    37: "Ивановская область",
    38: "Иркутская область",
    39: "Калининградская область",
    40: "Калужская область",
    41: "Камчатский край",
    42: "Кемеровская область",
    43: "Кировская область",
    44: "Костромская область",
    45: "Курганская область",
    46: "Курская область",
    47: "Ленинградская область",
    48: "Липецкая область",
    49: "Магаданская область",
    50: "Московская область",
    51: "Мурманская область",
    52: "Нижегородская область",
    53: "Новгородская область",
    54: "Новосибирская область",
    55: "Омская область",
    56: "Оренбургская область",
    57: "Орловская область",
    58: "Пензенская область",
    59: "Пермский край",
    60: "Псковская область",
    61: "Ростовская область",
    62: "Рязанская область",
    63: "Самарская область",
    64: "Саратовская область",
    65: "Сахалинская область",
    66: "Свердловская область",
    67: "Смоленская область",
    68: "Тамбовская область",
    69: "Тверская область",
    70: "Томская область",
    71: "Тульская область",
    72: "Тюменская область",
    73: "Ульяновская область",
    74: "Челябинская область",
    75: "Забайкальский край",
    76: "Ярославская область",
    77: "г. Москва",
    78: "г. Санкт-Петербург",
    79: "Еврейская автономная область",
    83: "Ненецкий автономный округ",
    86: "Ханты-Мансийский автономный округ — Югра",
    87: "Чукотский автономный округ",
    89: "Ямало-Ненецкий автономный округ"
}

fine_stats["region_name"] = fine_stats["region_id"].map(region_mapping)
fine_stats = fine_stats[["region_id", "region_name", "count", "mean", "median", "max"]]

fine_stats.to_csv("region_fine_stats.csv", index=False)

total = fine_stats["count"].sum()
print("Сумма:", total)
