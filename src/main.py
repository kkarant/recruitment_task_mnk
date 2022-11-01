from ftplib import FTP
import dotenv
import os
import patoolib

from config import DatabaseSettings, FTPSettings
from service import insert_csv_data_to_db
from database.base import BaseDatabase
from database.crud import \
    DataManager, PriceManager, DepositManager, QualityManager, WeightManager


def list_files(ftp):
    data = []
    ftp.dir(data.append)
    ftp.quit()
    for line in data:
        print("-", line)
    print(ftp.pwd())


def receive_file(filename, ftp):
    with open("data/" + filename, 'wb') as f:
        ftp.retrbinary(f"RETR {filename}", f.write)


def unpack_file(filename):
    patoolib.extract_archive("data/" + filename, outdir="data/rar_content")


def init_managers(db_config: DatabaseSettings) -> tuple[BaseDatabase, ...]:
    data_manager = DataManager(db_config)
    price_manager = PriceManager(db_config)
    deposit_manager = DepositManager(db_config)
    quality_manager = QualityManager(db_config)
    weight_manager = WeightManager(db_config)

    return (
        data_manager, price_manager, deposit_manager,
        quality_manager, weight_manager
    )


def main():
    dotenv.load_dotenv(".env")
    db_config = DatabaseSettings()
    BaseDatabase(db_config).createTables()

    (data_manager, price_manager, deposit_manager,
     quality_manager, weight_manager) = init_managers(db_config)

    files = {
        data_manager: ('data/rar_content/data.csv', ";"),
        deposit_manager: ('data/rar_content/deposit.csv', ";"),
        price_manager: ('data/rar_content/price.csv', ";"),
        quality_manager: ('data/rar_content/quantity.csv', ";"),
        weight_manager: ('data/rar_content/weight.txt', "\t")
    }

    for manager, file_data in files.items():
        insert_csv_data_to_db(file_data, manager)

    # with FTP(os.environ['IP']) as ftp:
    #     ftp.login(user=os.environ['LOGIN'], passwd=os.environ['PASSWORD'])
    #     # list_files(ftp)
    #     # receive_file("task.rar", ftp)
    #     ftp.quit()
    # unpack_file("task.rar")


if __name__ == '__main__':
    main()
