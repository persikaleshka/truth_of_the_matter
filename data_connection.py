import pandas as pd

df_old = pd.read_csv("unprocessed_data/unprocessed_data.csv", delimiter=";")  
df_new_spb = pd.read_csv("unprocessed_data/unprocessed_data_spb.csv", delimiter=";")
df_new_msc = pd.read_csv("unprocessed_data/unprocessed_data_msc.csv", delimiter=";")
df_new_len = pd.read_csv("unprocessed_data/unprocessed_data_len.csv", delimiter=";")
df_hntsv = pd.read_csv("unprocessed_data/unprocessed_data_hntsv.csv", delimiter=";")
df_ps = pd.read_csv("unprocessed_data/unprocessed_data_ps.csv", delimiter=";")
df_kmo = pd.read_csv("unprocessed_data/unprocessed_data_kmo.csv", delimiter=";")
df_vii = pd.read_csv("unprocessed_data/unprocessed_data_vii.csv", delimiter=";")
df_kkk = pd.read_csv("unprocessed_data/unprocessed_data_kkk.csv", delimiter=";")
df_oop = pd.read_csv("unprocessed_data/unprocessed_data_oop.csv", delimiter=";")
df_pss = pd.read_csv("unprocessed_data/unprocessed_data_pss.csv", delimiter=";")
df_stt = pd.read_csv("unprocessed_data/unprocessed_data_stt.csv", delimiter=";")
df_tuac = pd.read_csv("unprocessed_data/unprocessed_data_tuac.csv", delimiter=";")

regions_to_remove = ["77", "78", "50", "47", "27", "34", "54", "64", "69", "25", "26", "51", "46", "55", "37", "38", "42", "43", "45", "56", "57", "58", "59", "63", "65", "66", "68", "70", "72", "73", "76"]
df_filtered = df_old[~df_old["region"].isin(regions_to_remove)]

df = pd.concat([df_filtered, df_new_msc], ignore_index=True)
df = pd.concat([df, df_new_spb], ignore_index=True)
df = pd.concat([df, df_new_len], ignore_index=True)
df = pd.concat([df, df_hntsv], ignore_index=True)
df = pd.concat([df, df_ps], ignore_index=True)
df = pd.concat([df, df_kmo], ignore_index=True)
df = pd.concat([df, df_vii], ignore_index=True)
df = pd.concat([df, df_kkk], ignore_index=True)
df = pd.concat([df, df_oop], ignore_index=True)
df = pd.concat([df, df_pss], ignore_index=True)
df = pd.concat([df, df_stt], ignore_index=True)
df = pd.concat([df, df_tuac], ignore_index=True)

df.to_csv("unprocessed_data/unprocessed_data_all.csv", index=False)