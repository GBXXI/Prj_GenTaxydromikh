
import sqlite3 as sq3
import os

def select_(db):
    curr = db.cursor()
    val = curr.execute(
        """
            --sql
            SELECT * 
            FROM 
                sqlite_master
            WHERE
                type = 'table' AND
                name NOT LIKE 'sqlite_%'
            ;
        """
    )
    curr.close()
    return val

if __name__ == "__main__":
    db_file = "./GenikhTaxydromikh.db"
    # conn = sq3.connect(db_file)
    with sq3.connect(db_file) as conn:
        t = select_(conn)
    
    print(t)
