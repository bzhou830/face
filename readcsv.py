import pandas as pd
df = pd.read_csv("C:\\Users\\Bz\\Desktop\\ML\\dataset\\dataset\\celeba\\labels.csv", sep='\t', usecols=[1, 2])

for row in df.itertuples():
    print(getattr(row, 'img_name'), getattr(row, 'gender')) # 输出每一行
print(type(df))