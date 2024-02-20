import os
from pathlib import Path

import psycopg2
import pandas as pd


class DBHandler:
    TABLE_NAME = "repos2"

    def __init__(self) -> None:
        self.engine = None
        self.base_dir = Path(__file__).resolve().parent.parent
        self.scripts_dir = self.base_dir / "scripts"
        self.create_script_path = self.scripts_dir / "create.sql"

    def _connect(self) -> None:
        if self.engine:
            return

        host = os.environ["DB_HOST"]
        port = os.environ["DB_PORT"]
        database = os.environ["DB_NAME"]
        username = os.environ["DB_USERNAME"]
        password = os.environ["DB_PASSWORD"]

        self.engine = psycopg2.connect(
            host=host,
            dbname=database,
            user=username,
            password=password,
            port=port
        )

    def _disconnect(self) -> None:
        if not self.engine:
            return

        self.engine.close()

    # def populate(self, df: pd.DataFrame) -> None:
    #     self._connect()
    #     self._create_table()
    #
    #     with self.engine.cursor() as cur:
    #         # get current ids
    #         cur.execute(f"SELECT id FROM {self.TABLE_NAME}")
    #         records = cur.fetchall()
    #         ids = [record[0] for record in records]
    #
    #         # get ids from dataframe not in the table
    #         df_new = df[~df["id"].isin(ids)]
    #
    #         # if there are new ids
    #         if not df_new.empty:
    #             # prepare data and insert into table
    #             data_tuples = [tuple(x) for x in df_new.to_numpy()]
    #             fields_list = [
    #                 "id",
    #                 "name",
    #                 "description",
    #                 "created_at",
    #                 "updated_at",
    #                 "html_url",
    #             ]
    #             fields = ",".join(fields_list)
    #             sql_stmt = "INSERT INTO {} ({}) VALUES {}"
    #             insert_query = sql.SQL(sql_stmt.format(
    #                 self.TABLE_NAME,
    #                 fields,
    #                 sql.SQL(',').join(map(sql.Literal, data_tuples))
    #             ))
    #             cur.execute(insert_query)
    #             self.engine.commit()
    #
    #     self._disconnect()

    def populate(self, df: pd.DataFrame) -> None:
        self._connect()
        self._create_table()

        with self.engine.cursor() as cur:
            cur.execute(f"SELECT id FROM {self.TABLE_NAME}")
            existing_ids = {row[0] for row in cur.fetchall()}

            new_data = df[~df["id"].isin(existing_ids)]

            if not new_data.empty:
                fields_list = [
                    "id",
                    "name",
                    "description",
                    "created_at",
                    "updated_at",
                    "html_url",
                ]
                fields = ",".join(fields_list)
                values = ",".join(["%s"] * len(fields_list))
                data_tuples = [tuple(row) for row in
                               new_data[fields_list].values]
                sql_stmt = (f"INSERT INTO "
                            f"{self.TABLE_NAME} "
                            f"({fields}) "
                            f"VALUES "
                            f"({values})")
                try:
                    cur.executemany(sql_stmt, data_tuples)
                    self.engine.commit()
                except psycopg2.Error as e:
                    print(f"Error inserting data: {e}")
                    self.engine.rollback()

        self._disconnect()

    def _create_table(self):
        with self.engine.cursor() as cur:
            with open(self.create_script_path, "r") as fh:
                sql_stmt = fh.read()
                cur.execute(sql_stmt)
            self.engine.commit()
