from .base import BaseDatabase


class DataManager(BaseDatabase):
    def insert(self, data, cur, conn) -> None:
        insertStr = f'''INSERT INTO DATA_ 
                         VALUES (%s ,%s, %s, %s, %s)'''

        cur.execute(insertStr, data)
        conn.commit()


class DepositManager(BaseDatabase):
    def insert(self, data, cur, conn) -> None:
        insertStr = f'''INSERT INTO DEPOSIT_ 
                        VALUES (%s ,%s)'''
        cur.execute(insertStr, data)
        conn.commit()


class PriceManager(BaseDatabase):
    def insert(self, data, cur, conn) -> None:
        insertStr = f'''INSERT INTO PRICE_ 
                        VALUES (%s ,%s)'''
        cur.execute(insertStr, data)
        conn.commit()


class QualityManager(BaseDatabase):
    def insert(self, data, cur, conn) -> None:
        insertStr = f'''INSERT INTO QUANTITY_ 
                        VALUES (%s ,%s, %s)'''
        cur.execute(insertStr, data)
        conn.commit()


class WeightManager(BaseDatabase):
    def insert(self, data, cur, conn) -> None:
        insertStr = f'''INSERT INTO WEIGHT_ 
                            VALUES (%s ,%s, %s)'''
        cur.execute(insertStr, data)
        conn.commit()
