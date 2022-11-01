import os

import dotenv

from config import DatabaseSettings, FTPSettings
from database.base import BaseDatabase
from database.crud import \
    DataManager, PriceManager, DepositManager, QualityManager, WeightManager, ReportManager
from service.csv_service import report_to_csv, insert_csv_data_to_db
from service.ftp_service import receive_file_manager, send_file


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
    db_base = BaseDatabase(db_config)
    db_base.createTables()
    (data_manager, price_manager, deposit_manager,
     quality_manager, weight_manager) = init_managers(db_config)

    ftp_config = FTPSettings()
    path = "./data/rar_content"
    os.makedirs(path, exist_ok=True)
    filename = 'task.rar'
    files = {
        data_manager: ('data/rar_content/data.csv', ";"),
        deposit_manager: ('data/rar_content/deposit.csv', ";"),
        price_manager: ('data/rar_content/price.csv', ";"),
        quality_manager: ('data/rar_content/quantity.csv', ";"),
        weight_manager: ('data/rar_content/weight.txt', "\t")
    }

    receive_file_manager(ftp_config, filename)

    for manager, file_data in files.items():
        insert_csv_data_to_db(file_data, manager)

    rManager = ReportManager(db_config)
    with rManager.transaction() as session:
        cur, conn = session
        db_base.alterTable(cur, conn)
        rManager.reportGenerator(cur, conn)
        report = rManager.select(cur, conn)
        report_to_csv(report)
    send_file(ftp_config, filename='report_Mykyta_Karant.csv')


if __name__ == '__main__':
    main()
