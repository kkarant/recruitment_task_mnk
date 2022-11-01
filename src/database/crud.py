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


class ReportManager(BaseDatabase):
    def insert(self, data, cur, conn) -> None:
        insertStr = f'''INSERT INTO REPORT_ 
                            VALUES (%s ,%s, %s, %s ,%s, %s, %s ,%s, %s)'''
        cur.execute(insertStr, data)
        conn.commit()

    def reportGenerator(self, cur, conn):
        insertStr = f'''insert into report_ 
        (part_number, main_part_number, manufacturer, category_, origin, price, deposit, overall_price, quantity)
        select d.part_number, d.main_part_number, d.manufacturer, 
        d.category_, d.origin, p.price, coalesce(d2.deposit, 0) 
        as deposit, (p.price + d2.deposit) as overall_price, coalesce(q.quantity, 0) as quantity from data_ d
        left join price_ p on d.part_number = p.part_number 
        left join deposit_ d2 on d.part_number = d2.part_number 
        left join quantity_ q on d.part_number = q.part_number
        where q.warehouse in ('A', 'H', 'J', '3', '9') and q.quantity != 0 and p.price + d2.deposit >= 2;'''
        cur.execute(insertStr)
        conn.commit()
