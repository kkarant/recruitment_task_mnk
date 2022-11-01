from ftplib import FTP
import dotenv
import os
import patoolib

from config import DatabaseSettings, FTPSettings
from service import csv_to_dataframe
from database.base import BaseDatabase


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


def main():
    files = [('data/rar_content/data.csv', ";"), ('data/rar_content/deposit.csv', ";"), ('data/rar_content/price.csv', ";"),
             ('data/rar_content/quantity.csv', ";"), ('data/rar_content/weight.txt', "\t")]

    dotenv.load_dotenv(".env")

    db_config = DatabaseSettings()
    db_manager = BaseDatabase(db_config)
    ftp_config = FTPSettings()

    # with FTP(os.environ['IP']) as ftp:
    #     ftp.login(user=os.environ['LOGIN'], passwd=os.environ['PASSWORD'])
    #     # list_files(ftp)
    #     # receive_file("task.rar", ftp)
    #     ftp.quit()
    # unpack_file("task.rar")

    db_manager.createTables()
    csv_to_dataframe(files)


if __name__ == '__main__':
    main()
