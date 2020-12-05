
import os
import sqlite3 as lite3
import logging


# ------------------------------MODULARISED LOGGER------------------------------
directory = os.getcwd()
file_handler = logging.FileHandler(f"{directory}/GenikhTaxydromikh.log")

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

log_format = logging.Formatter('%(asctime)s %(levelname)s\n%(message)s\n')

file_handler.setFormatter(log_format)

log.addHandler(file_handler)


class DatebaseQueries():

    def __init__(self, conn, tbname):
        self.tbname = tbname
        self.conn = conn

    @property
    def show_tables(self):
        try:
            curr = self.conn.cursor()

            tables = curr.execute(
                f"""
                    SELECT name FROM sqlite_master;
                """
            )

            table_list = [table[0] for table in tables]

        except Exception as err:
            log.warning(f'Tables Show Error:\n\t{err}')
        finally:
            curr.close()
            return table_list

    @property
    def select_headers(self):
        curr = self.conn.cursor()

        try:
            headers = curr.execute(
                f"""
                    SELECT name FROM PRAGMA_TABLE_INFO('{self.tbname}');
                """
            )

            for header in headers:
                yield header

        except Exception as err:
            log.warning(f'Headers Select Error:\n\t{err}')

        finally:
            curr.close()

    def select_emails(self, headers=None):
        curr = self.conn.cursor()

        if headers == None:
            self.headers = self.select_headers
        else:
            self.headers = [(headers,)]

        try:
            for header in self.headers:
                emails = curr.execute(
                    f"""
                        SELECT DISTINCT
                            {header[0]}
                        FROM
                            {self.tbname}
                        WHERE
                            {header[0]} IS NOT NULL;
                    """
                )

                for email in emails:
                    yield email

        except Exception as err:
            print('Emails Select Error:\n\t', err)

        finally:
            self.headers = self.select_headers  # Reseting our headers.
            curr.close()

    def email_insert(self, header, values):
        curr = self.conn.cursor()

        # All the headers are used in order for the insertion to be executed by
        # placeholders.
        table = {
            headers[0]:
            value if header == headers[0] else None for value in values
            for headers in self.select_headers
        }

        placeholders = ['?' for header in table.keys()]
        placeholders = ', '.join(f'{qm}' for qm in placeholders)

        if header in table.keys():
            try:
                insertion = (
                    f"""
                        INSERT INTO
                            {self.tbname}(
                                {', '.join(f"{header}" for header in table.keys())}
                            )
                        VALUES
                            ({placeholders});

                    """
                )

                curr.execute(insertion, list(table.values()))

            except Exception as err:
                log.warning(f'Insertion Error:\n\t{err}')

            finally:
                curr.close()
                self.conn.commit()

        else:
            try:
                curr.execute(
                    f"""
                        ALTER TABLE
                            {self.tbname}
                        ADD COLUMN
                            {header} text;
                    """
                )

            except Exception as err:
                log.warning(f'Expansion Error:\n\t{err}')

            finally:
                self.conn.commit()
                self.email_insert(header, values)

    def email_delete(self, header, values):
        curr = self.conn.cursor()

        try:
            curr.execute(
                f"""
                    DELETE FROM
                        {self.tbname}
                    WHERE
                        {header} = '{values}';
                """
            )
        except Exception as err:
            log.warning(f'Deletion Error:\n\t{err}')
        finally:
            curr.close()
            self.conn.commit()

    def email_update(self, header, value_replaced, replacing_value):
        curr = self.conn.cursor()

        try:
            curr.execute(
                f"""
                    UPDATE
                        {self.tbname}
                    SET
                        {header} = '{replacing_value}'
                    WHERE
                        {header} = '{value_replaced}';
                """
            )

        except Exception as err:
            log.warning(f'Update Error:\n\t{err}')
        finally:
            curr.close()
            self.conn.commit()

    def __repr__(self):
        return f"DatebaseQueries({self.conn}, {self.tbname})"

    def __str__(self):
        return (
            f"Database: {os.path.basename(self.conn)}\n"
            f"Table: {self.tbname}"
        )


class DataBase(DatebaseQueries):

    def __init__(self, db):
        self.db = db
        self.conn = lite3.connect(self.db)

    def table(self, tbname):
        self.tbname = tbname
        return DatebaseQueries(self.conn, self.tbname)

    def __enter__(self):
        # self.conn = lite3.connect(self.db)
        return self

    def __repr__(self):
        return f"DataBase({self.db})"

    def __str__(self):
        return (
            f"Database: {os.path.basename(self.db)}"
        )

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            # self.conn.commit()
            self.conn.close()
        else:
            log.warning(f"{exc_type}, {exc_val}, {exc_tb}")


# -------------------------------"Dirty Testing"--------------------------------
if __name__ == "__main__":
    # pass

    # ------------------------------------------------------------------------------
    # db_file = "./GenikhTaxydromikh.db"
    # conn = lite3.connect(db_file)

    # db_class = DbElements(db_file, 'stores')
    # emails = db_class.select_emails
    # headers = db_class.select_headers()

    # dict_ = dict()
    # for header in headers:
    #     dict_.update({header[0] : [email[0] for email in emails(header)]})
    # print(dict_)
    # ------------------------------------------------------------------------------
    directory = os.getcwd()
    db_file = (f"{directory}/GenikhTaxydromikh.db")
    db_prj = DataBase(db_file)
    db_query = DatebaseQueries(db_file, 'stores')
    # db_prj.table = 'stores'

    tb = db_prj.table('stores')
    print(db_prj.show_tables)
    # print(db_query)
    # print(repr(db_query))
    # tb.email_insert('AEO_NG_expand', ['georgebitsonis+ExpansionTest@gmail.com'])
    # tb.email_delete('AEO_NG', 'georgebitsonis+UPDATETest@gmail.com')
    tb.email_update('AEO_N5G', 'georgebitsonis+InsertionTest@gmail.com', 'georgebitsonis+UPDATETest@gmail.com')
    # print(tb.show_tables)
    # # # lb = tb.select_emails('AEO_NG')
    # # lb = tb.select_emails()
    # # h = [h[0] for h in lb]
    # # e = [header[0] for header in db_prj.select_headers]
    # # print(h)
    # # print(e)

    # with db_prj as db:
    #     table_stores = db.table('stores')
    #     table_office_team = db.table('officeteam')

    # j = table_stores.select_emails()

    # h1 = [[email[0] for email in table_stores.select_emails(header[0])] for header in table_stores.select_headers]
    # print(h1)

    # # self.stores = [header[0] for header in table_stores.select_headers]
    #     office_team = [email[0] for email in table_office_team.select_emails()]

    #     # stores = {header[0]:[email[0] for email in table_stores.select_emails(header)]\
    #     #     for header in table_stores.select_headers}


# ------------------------------------------------------------------------------
    # directory = os.getcwd()
    # db_file = (f"{directory}/GenikhTaxydromikh.db")
    # database = DataBase(db_file)

    # with database as db:
    #     headers = db.select_headers
    #     emails = db.select_emails

    #     with concurrent.futures.ThreadPoolExecutor() as executor:
    #         tb = ['stores', 'officeteam']
    #         results = executor.map(headers, tb)

    #     # with concurrent.futures.ThreadPoolExecutor() as executor:
    #     #     for result in results:
    #     #         result_1 = executor.map(emails, list(result))

    #     # for result in result_1:
    #     #     for inner_result in result:
    #     #         print(inner_result)
    #         for result in results:
    #             print(result)
