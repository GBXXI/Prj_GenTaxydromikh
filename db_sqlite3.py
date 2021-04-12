
import os
import sqlite3 as lite3
import logging
import re


# ------------------------------MODULARISED LOGGER------------------------------
directory = os.getcwd()
file_handler = logging.FileHandler(f"{directory}/GenikhTaxydromikh.log")

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

log_format = logging.Formatter(
    '%(filename)s '
    '%(asctime)s %(levelname)s\n'
    '%(funcName)s\n%(message)s\n'
)

file_handler.setFormatter(log_format)

log.addHandler(file_handler)


class DatabaseQueries():

    def __init__(self, conn, tbname):
        self.tbname = tbname
        self.conn = conn

    def update_view_cases_order(self, case):
        cur = self.conn.cursor()

        view = {
            "Recipients Email": ['Recipients', 'recipient_id', 'recipient_name'],
            "Included Email"  : ['CarbonCopy', 'included_id',  'included_name']
            }.get(self.tbname)

        ids_names = cur.execute(
            f"""
                SELECT {view[1]}, {view[2]}
                FROM {view[0]}
                ORDER BY {view[2]}
                ;
            """
        )

        for id_name in ids_names:
            substituted_input = re.sub("\'|;", " ", id_name[1]) # Eliminating non-acceptable characters.

            yield (
                {
                    "cases": f"(CASE WHEN e.email_id = {id_name[0]} THEN e.email END) '{substituted_input}'",
                    "order": f"'{substituted_input}' DESC"
                }.get(case)
            )

    def update_views(self):
        email_table = {
            "Recipients Email": "RecipientsEmail",
            "Included Email"  : "CarbonCopyEmails"
        }.get(self.tbname)
        try:
            with open(f"{os.getcwd()}/views.sql", 'w+') as view:
                view.write(
                    (
                        f"DROP VIEW IF EXISTS '{self.tbname}';\n"
                        f"CREATE VIEW IF NOT EXISTS '{self.tbname}' AS\n"
                        "SELECT DISTINCT\n"
                    )
                )
                view.write(',\n'.join(self.update_view_cases_order('cases')))
                view.write(f"\nFROM {email_table} e\n")
                view.write("ORDER BY ")
                view.write(',\n'.join(self.update_view_cases_order('order')))
                view.write('\n;')

        except Exception as err:
            log.warning(f'Writing view Error:\n\t{err}')

        try:
            cur = self.conn.cursor()
            with open(f"{os.getcwd()}/views.sql", "r") as view:
                new_view = view.read()
                cur.executescript(new_view)
                self.conn.commit()

        except Exception as err:
            log.warning(f'Reading view Error:\n\t{err}')

        finally:
            cur.close()

        try:
            os.remove(f"{os.getcwd()}/views.sql")

        except Exception as err:
            log.warning(f'Deleting view Error:\n\t{err}')

    @property
    def select_headers(self):
        cur = self.conn.cursor()
        self.update_views()

        try:
            headers = cur.execute(
                f"""
                    SELECT name FROM PRAGMA_TABLE_INFO('{self.tbname}');
                """
            )

            for header in headers:
                yield header

        except Exception as err:
            log.warning(f'Headers Select Error:\n\t{err}')

        finally:
            cur.close()

    def select_emails(self, headers=None):
        cur = self.conn.cursor()

        if headers == None:
            self.headers = self.select_headers
        else:
            self.headers = [(headers,)]

        try:
            for header in self.headers:
                emails = cur.execute(
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
            log.warning(err)

        finally:
            self.headers = self.select_headers  # Reseting our headers.
            cur.close()


    def email_insert(self, header, values):
        cur = self.conn.cursor()
        email_table = {
            "Recipients Email": ["Recipients", "RecipientsEmail", "recipient"],
            "Included Email"  : ["CarbonCopy", "CarbonCopyEmails", "included"]
        }.get(self.tbname)

        values = re.sub(";|\'|", "", values)
        header = re.sub(";|\'|", "", header)

        _id = cur.execute(
            f"""
                SELECT
                    {email_table[2]}_id
                FROM
                    {email_table[0]}
                WHERE
                    {email_table[2]}_name = '{header}'
                ;
            """
        )
        header_id = _id.fetchall()

        if header_id:
            cur.execute(
                f"""
                    INSERT INTO {email_table[1]}(
                            email_id, email
                        )

                        VALUES
                            ({header_id[0][0]}, '{values}')
                    ;
                """
            )

            self.conn.commit()

        else:
            cur.execute(
                f"""
                    INSERT INTO {email_table[0]}(
                            {email_table[2]}_name
                        )

                        VALUES
                            ('{header}')
                    ;
                """
            )

            self.conn.commit()
            # Recursion
            self.email_insert(header, values)

    def email_delete(self, header, values):
        cur = self.conn.cursor()
        email_table = {
            "Recipients Email": ["Recipients", "RecipientsEmail", "recipient"],
            "Included Email"  : ["CarbonCopy", "CarbonCopyEmails", "included"]
        }.get(self.tbname)

        values = re.sub(";|\'|", "", values)
        header = re.sub(";|\'|", "", header)

        _id = cur.execute(
            f"""
                SELECT
                    {email_table[2]}_id
                FROM
                    {email_table[0]}
                WHERE
                    {email_table[2]}_name = '{header}'
                ;
            """
        )
        header_id = _id.fetchall()

        if header_id:
            cur.execute(
                f"""
                    DELETE FROM
                        {email_table[1]}
                    WHERE
                        email_id = {header_id[0][0]} AND
                        email = '{values}'
                    ;
                """
            )

            self.conn.commit()

            elements = cur.execute(
                f"""
                    SELECT
                        COUNT(email_id)
                    FROM
                        {email_table[1]}
                    WHERE
                        email_id = {header_id[0][0]}
                    ;
                """
            )

            clear = elements.fetchall()


            if clear[0][0] == 0:
                cur.execute(
                    f"""
                        DELETE FROM
                            {email_table[0]}
                        WHERE
                            {email_table[2]}_id = {header_id[0][0]}

                        ;
                    """
                )

                self.conn.commit()


    def __repr__(self):
        return f"DatabaseQueries({self.conn}, {self.tbname})"

    def __str__(self):
        return (
            f"Database: {os.path.basename(self.conn)}\n"
            f"Table: {self.tbname}"
        )

class DataBase(DatabaseQueries):

    def __init__(self, db):
        self.db = db
        self.conn = lite3.connect(self.db)

    def setup(self):
        cur = self.conn.cursor()
        try:
            with open(f"{os.getcwd()}/setup.sql", "r") as setupfile:
                setup = setupfile.read()
                cur.executescript(setup)

        except Exception as err:
            log.warning(f'Setup Error:\n\t{err}')
            return False

        finally:
            cur.close()
        return True

    def table(self, tbname):
        self.tbname = tbname
        return DatabaseQueries(self.conn, self.tbname)

    @property
    def show_views(self):
        try:
            cur = self.conn.cursor()

            tables = cur.execute(
                f"""
                    SELECT name FROM sqlite_master
                    WHERE type='view';
                """
            )

            table_list = [table[0] for table in tables]

        except Exception as err:
            log.warning(f'Tables Show Error:\n\t{err}')
        finally:
            cur.close()
            return table_list


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


if __name__ == "__main__":
    # db_file = 'sqlite3_external\Main_test.db'
    db_file = r'sqlite3_external\Main_test.db'
    with DataBase(db_file) as db:
        cur = db.conn.cursor()
        k = db.table("Included Email")
        # db.tbname = "Recipients"se
        print(db.tbname)
        print(k.tbname)

        for header in k.select_headers:
            print(header)

    #    for email in k.select_emails():
    #        print(email)

        # for index, id_ in enumerate(k.update_view_cases()):
        #     print(index, id_)
        # k.update_views()
        k.email_insert(';Zaccaria Mmitr', 'email_insert@test.com')
        k.email_delete('Zaccaria Mmitr', 'email_insert@test.com')
