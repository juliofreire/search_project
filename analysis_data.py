import pandas as pd

filename_csv = ("houses_dict.csv")

df = pd.read_csv(filename_csv)

# print(df.head())

print(len(df))
df = df.drop_duplicates()
print(df.count().sum())

df.drop(columns="link")
print(df.head())