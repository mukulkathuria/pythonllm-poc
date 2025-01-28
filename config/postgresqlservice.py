import psycopg # type: ignore
import os
from decimal import Decimal


class PostgresService:
    def __init__(self) -> None:
        self.conn = psycopg.connect(
            dbname=os.environ['dbname'],
            user=os.environ['user'],
            password=os.environ['password'],
            host=os.environ['host'],
            port=os.environ['port'],
        )

    def query(self, query):
        cur = self.conn.cursor()
        cur.execute(query)
        rows = cur.fetchall()
        columns = [desc[0] for desc in cur.description]
        data = []
        for row in rows:
            row_data = {}
            for i, column in enumerate(columns):
                if isinstance(row[i], Decimal):
                    row_data[column] = str(row[i])
                else:
                    row_data[column] = row[i]
            data.append(row_data)
        # json_data = json.dumps(data, indent=4)
        cur.close()
        return data
        # self.conn.close()
