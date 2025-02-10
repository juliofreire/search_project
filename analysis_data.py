import pandas as pd


filename_csv = ("houses_dict.csv")

df = pd.read_csv(filename_csv)

print(df.head())