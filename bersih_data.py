import pandas as pd

path = 'hasil\\scrape_shopee.csv'
path_result = 'hasil\\scrape_shopee_clean.csv'
index = 'comment'

try:
    df = pd.read_csv(path) 
    df = df[df[index].notna()]
    df = df.drop_duplicates()

    print(df)
    df.to_csv(path_result, index=False)
    print('\nData Telah Tersimpan')
except:
    print('Data Tidak Ditemukan')