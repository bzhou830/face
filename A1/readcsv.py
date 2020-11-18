import pandas as pd
df = pd.read_csv("D:/123456/ML/dataset/dataset/cartoon_set/labels.csv", sep='\t', usecols=[1, 2])

for row in df.itertuples():
    print(getattr(row, 'img_name'), getattr(row, 'gender')) # 输出每一行
print(type(df))