import pandas as pd
import numpy as np
from database import mysql_engine, pg_engine
import clickhouse_connect

data = pd.read_csv("AI_SocialMedia_Student_Health_Dataset_clean.csv")
df = pd.DataFrame(data)

# Colomn Age
# membagi kategori usia remaja dan dewasa <20 & >= 20
# df['Age_Category'] = np.where(df['Age'] < 20, "Remaja", "Dewasa")

# Colomn Gender
# mengubah gender menjadi hanya male dan female dengan acuan count terbanyak
# count_gender = df['Gender'].value_counts()
# count_gender_max = count_gender.idxmax()
# df['Gender_Fix'] = df['Gender'].replace("Non-binary", count_gender_max)

# Column Daily_Social_Media_Hours
# DSMH_Mean = df['Daily_Social_Media_Hours'].mean()

# mengubah Daily_Social_Media_Hours menjadi category
# bins = [0, 2.5, 5, 24]
# labels = ['Low', 'Moderate', 'High']
# df['Social_Media_Hours_Category'] = pd.cut(df['Daily_Social_Media_Hours'].replace(0, DSMH_Mean), bins=bins, labels=labels)

# Column Daily_AI_Tool_Usage_Hours
# DATUH_Mean = df['Daily_AI_Tool_Usage_Hours'].mean()

# mengubah Daily_AI_Tool_Usage_Hours menjadi category
# bins = [0, 5, 10, 24]
# labels = ['Low', 'Moderate', 'High']
# df['AI_Tool_Usage_Category'] = pd.cut(df['Daily_AI_Tool_Usage_Hours'].replace(0, DATUH_Mean), bins=bins, labels=labels)

# mengubah Sleep_Hours menjadi category (Good & Bad)
# bins = [0, 7, 10, 24]
# label = ["Bad", "Good", "Not Good"]
# df['Sleep_Hours_Category'] = pd.cut(df["Sleep_Hours"], bins=bins, labels=label)

# mengubah Physical_Activity_Hours yang bernilai 0
# PAH_Mean = df['Physical_Activity_Hours'].mean()
# df['Physical_Activity_Hours_New'] = np.where(df['Physical_Activity_Hours'] < 0.1, PAH_Mean, df['Physical_Activity_Hours'])

# mengubah Mental_Health_Score dengan category Bad & Good
# df['Mental_Health_Score_New'] = np.where(df['Mental_Health_Score']< 76, "Bad", "Good")

# mengubah Physical_Health_Score dengan category Bad & Good
# df['Physical_Health_Score_New'] = np.where(df['Physical_Health_Score']< 76, "Bad", "Good")

# mengubah Academic_Performance_Score dengan category Bad & Good
# df['Academic_Performance_Score_New'] = np.where(df['Academic_Performance_Score']< 76, "Bad", "Good")

print("DATASET :")
print(df.head(10))
# print(PAH_Mean)

# MYSQL
print("\n--- Mengirim Data ke Mysql ---")
try:
    df.to_sql(name='Hasil_Transformasi', con=mysql_engine, if_exists='replace', index=False)
    print("Data berhasil create di Database Mysql Docker")
except Exception as e:
    print(f"Gagal Input ke database: \n{e}")

# POSTGRES
print("\n--- Mengirim Data ke Postgres ---")
try:
    df.to_sql(name='Hasil_Transformasi', con=pg_engine, if_exists='replace', index=False)
    print("Data berhasil create di Database Postgres Docker")
except Exception as e:
    print(f"Gagal Input ke database: \n{e}")

# # CLICKHOUSE
# print("\n--- Mengirim Data ke Clickhouse ---")
# try:
#     client = clickhouse_connect.get_client(
#         host='localhost',
#         port=8123,
#         username='clickhouse',
#         password='adminpass123',
#         database='tes_clickhouse'
#     )
#     client.insert_df(table='Hasil_Transformasi', df=df)
#     print("Data berhasil create di Database Clickhouse Docker")
# except Exception as e:
#     print(f"Gagal Input ke database: \n{e}")