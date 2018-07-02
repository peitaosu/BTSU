import os
import sys
import sqlite3


def merge(db_a, db_b):
    conn_a = sqlite3.connect(db_a)
    conn_a.text_factory = str
    c_a = conn_a.cursor()

    conn_b = sqlite3.connect(db_b)
    conn_b.text_factory = str
    c_b = conn_b.cursor()

    c_b.execute("SELECT * FROM torrent")
    for row in c_b.fetchall():
        c_a.execute(
            '''INSERT OR IGNORE INTO torrent(hash, name, magnet, info) VALUES (?, ?, ?, ?);''', row)
    conn_a.commit()

    conn_a.close()
    conn_b.close()

if __name__=="__main__":
    if len(sys.argv) < 3:
        print "python mergedb.py <a.db> <b.db>"
    db_a = sys.argv[1]
    db_b = sys.argv[2]
    merge(db_a, db_b)