import psycopg2
from config import DatabaseSettings
from contextlib import contextmanager


class BaseDatabase:
    def __init__(self, db_config: DatabaseSettings):
        self.config = db_config

    @contextmanager
    def transaction(self):
        conn = psycopg2.connect(
            database=self.config.database,
            user=self.config.user,
            password=self.config.password,
            host=self.config.host,
            port=self.config.port
        )
        cur = conn.cursor()
        try:
            yield cur, conn
        finally:
            cur.close()
            conn.close()

    @staticmethod
    def createTableData(cur, conn):
        cur.execute(f'''create table if not exists DATA_(
                             part_number  varchar(10) not null,
                             manufacturer varchar(45) not null,
                             main_part_number varchar(45) not null,
                             category_ varchar(255) not null,
                             origin varchar(10) not null
                            )''')
        conn.commit()

    @staticmethod
    def createTableDeposit(cur, conn):
        cur.execute(f'''create table if not exists DEPOSIT_(
                             part_number varchar(10) not null,
                             deposit varchar(10) not null
                            )''')
        conn.commit()

    @staticmethod
    def createTablePrice(cur, conn):
        cur.execute(f'''create table if not exists PRICE_(
                             part_number  varchar(10) not null,
                             price varchar(10) not null
                            )''')
        conn.commit()

    @staticmethod
    def createTableQuantity(cur, conn):
        cur.execute(f'''create table if not exists QUANTITY_(
                             part_number  varchar(10) not null,
                             quantity varchar(10) not null,
                             warehouse varchar(10) not null
                            )''')
        conn.commit()

    @staticmethod
    def createTableWeight(cur, conn):
        cur.execute(f'''create table if not exists WEIGHT_(
                             part_number  varchar(10) not null,
                             weight_unpacked varchar(10) not null,
                             weight_packed varchar(10) not null
                            )''')
        conn.commit()

    def createTables(self):
        with self.transaction() as database:
            cur, conn = database
            self.createTableData(cur, conn)
            self.createTableDeposit(cur, conn)
            self.createTablePrice(cur, conn)
            self.createTableQuantity(cur, conn)
            self.createTableWeight(cur, conn)

    def insert(self, data, cur, conn):
        raise NotImplementedError

