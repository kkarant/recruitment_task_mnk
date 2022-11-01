import pandas as pd


def csv_to_dataframe(files):
    for f in files:
        print(f)
        df = pd.read_csv(f[0], sep=f[1], header=0)
        print(df)
        df_sql(df)


def df_sql(df):
    for index, row in df.iterrows():
        data = row.tolist()



