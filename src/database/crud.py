from .base import BaseDatabase


class DataInsert(BaseDatabase):

    @staticmethod
    def insertData(data, cur, conn):
        insertStr = f'''INSERT INTO DATA_ 
                        VALUES (%s ,%s, %s, %s, %s)'''

        cur.execute(insertStr, data)
        conn.commit()

    @staticmethod
    def insertDeposit(data, cur, conn):
        insertStr = f'''INSERT INTO DEPOSIT_ 
                        VALUES (%s ,%s)'''
        cur.execute(insertStr, data)
        conn.commit()

    @staticmethod
    def insertPrice(data, cur, conn):
        insertStr = f'''INSERT INTO PRICE_ 
                        VALUES (%s ,%s)'''
        cur.execute(insertStr, data)
        conn.commit()

    @staticmethod
    def insertQuantity(data, cur, conn):
        insertStr = f'''INSERT INTO QUANTITY_ 
                        VALUES (%s ,%s, %s)'''
        cur.execute(insertStr, data)
        conn.commit()

    @staticmethod
    def insertWeight(data, cur, conn):
        insertStr = f'''INSERT INTO WEIGHT_ 
                            VALUES (%s ,%s, %s)'''
        cur.execute(insertStr, data)
        conn.commit()
