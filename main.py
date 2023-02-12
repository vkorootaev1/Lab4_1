import re

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math
import scipy.stats as stats


pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.max_colwidth', None)
pd.options.display.expand_frame_repr = False

# Подготовка данных
df = pd.read_csv('drinks.csv')

numeric_cols = [col for col in df.columns if pd.api.types.is_numeric_dtype(df[col].dtype) and col != 'index']

df[numeric_cols] = df[numeric_cols].replace(0.0, np.nan)

# 1.1.
print('\n\nИзначально: ')
print(df.info())

# Удаление колонок, в которых больше 10% пропусков
df = df.dropna(axis='columns', thresh=int(0.9 * len(df)), inplace=False)

print('\n\nПосле удаления колонок: ')
print(df.info())

# Количество пропусков в каждой колонке
gaps_df = pd.DataFrame(((col, df[col].dtype, df[col].isna().sum()) for col in df),
                       columns=["column", "type", "na_count"])

print('\n\nКоличество пропусков в каждой колонке: ')
print(gaps_df)

# Числовые колонки
numeric_cols = [col for col in df.columns if pd.api.types.is_numeric_dtype(df[col].dtype) and col != 'index']
print('\n\nЧисловые колонки: ')
print(numeric_cols)

# Заполнение пустых значений средним значением
for col in numeric_cols:
    df[col].fillna(value=df[col].mean(), inplace=True)

print('\n\nПосле заполнения пустых значений средним: ')
print(df.info())

# 1.2.

# Ящик с усами до работы с выбросами
plt.rcParams["figure.figsize"] = 12, 6
df[numeric_cols].boxplot()
plt.show()

# Столбцы в которых есть выбросы
outliers = ['spirit_servings', 'total_litres_of_pure_alcohol']


for x in outliers:

    q25 = df[x].quantile(0.25)
    q75 = df[x].quantile(0.75)
    IQR = q75 - q25
    df.loc[df[x] < (q25 - (1.5 * IQR)), x] = df[x].quantile(0.01)
    df.loc[df[x] > (q75 + (1.5 * IQR)), x] = df[x].quantile(0.99)

# Ящик с усами после работы с выбросами
plt.rcParams["figure.figsize"] = 12, 6
df[numeric_cols].boxplot()
plt.show()


# 1.3.

plt.subplot(2, 3, 1)
plt.scatter(df['index'], df['beer_servings'])
plt.title("beer_servings(scatter plot)")

plt.subplot(2, 3, 2)
plt.scatter(df['index'], df['spirit_servings'])
plt.title("spirit_servings(scatter plot)")

plt.subplot(2, 3, 3)
plt.scatter(df['index'], df['total_litres_of_pure_alcohol'])
plt.title("total_litres(scatter plot)")

plt.subplot(2, 3, 4)
plt.boxplot(df['beer_servings'])
plt.title("beer_servings(boxplot)")

plt.subplot(2, 3, 5)
plt.boxplot(df['spirit_servings'])
plt.title("spirit_servings(boxplot)")

plt.subplot(2, 3, 6)
plt.boxplot(df['total_litres_of_pure_alcohol'])
plt.title("total_litres(boxplot)")

plt.show()

