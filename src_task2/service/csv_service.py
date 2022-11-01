import csv
import threading
from typing import TypeAlias

import numpy as np
import pandas as pd
from pandas import DataFrame

from database.base import BaseDatabase

file: TypeAlias = str
sep: TypeAlias = str


def csv_to_dataframe(file_data: tuple[file, sep]) -> DataFrame:
    return pd.read_csv(file_data[0], sep=file_data[1], header=0)


def insert_df_data(df: DataFrame, manager: BaseDatabase) -> None:
    with manager.transaction() as session:
        cur, conn = session
        i = 0

        for index, row in df.iterrows():
            data = row.tolist()
            # print(data)
            i = i + 1
            print(f'row {i}')
            manager.insert(data, cur, conn)


def insert_df_data_threads(df: DataFrame, manager: BaseDatabase) -> None:
    n_threads = 10
    df_split = np.array_split(df, n_threads)
    with manager.transaction() as session:
        cur, conn = session

        threads = []

        for df in df_split:
            thread = threading.Thread(
                target=_insert_data, args=(df, manager, cur, conn)
            )
            threads.append(thread)
            thread.start()

        for index, thread in enumerate(threads):
            thread.join()
            print(f'{index} thread end')


def _insert_data(df, manager, cur, conn):
    i = 0
    sh = df.size
    for index, row in df.iterrows():
        i = i + 1
        print(f'row {i} of {sh}')
        data = row.tolist()

        manager.insert(data, cur, conn)


def insert_csv_data_to_db(file_data: tuple[file, sep], manager: BaseDatabase) -> None:
    df = csv_to_dataframe(file_data)
    print(file_data[0])
    insert_df_data_threads(df, manager)


def report_to_csv(report):
    with open('./data/report_Mykyta_Karant.csv', 'w', encoding='utf8', newline='') as r:
        csv_out = csv.writer(r, delimiter=',')
        csv_out.writerow(['main_part_number', 'manufacturer',
                          'category', 'origin', 'price', 'deposit', 'overall_price', 'quantity'])
        for row in report:
            csv_out.writerow(row)