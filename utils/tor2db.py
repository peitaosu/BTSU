import os
import sys
import subprocess
import sqlite3

def get_name(tor_file_path):
    cmd = ['transmission-show ' + tor_file_path]
    output = subprocess.Popen(
        cmd, stdout=subprocess.PIPE, shell=True).communicate()[0]
    return output.split('\n')[0][6:]


def get_magnet(tor_file_path):
    cmd = ['transmission-show -m ' + tor_file_path]
    output = subprocess.Popen(
        cmd, stdout=subprocess.PIPE, shell=True).communicate()[0]
    return output


def get_info(tor_file_path):
    cmd = ['transmission-show ' + tor_file_path]
    output = subprocess.Popen(
        cmd, stdout=subprocess.PIPE, shell=True).communicate()[0]
    return '\n'.join(output.split('\n')[3:])

def tor2db(tor_path, db_path, tor_hash_start):
    conn = sqlite3.connect(db_path)
    conn.text_factory = str
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS `torrent` (`hash` VARCHAR(40) NOT NULL, `name` TEXT NOT NULL, `magnet` TEXT NOT NULL, `info` TEXT NOT NULL, PRIMARY KEY(`hash`))''')
    conn.commit()
    for tor_file in os.listdir(tor_path):
        if not tor_file.endswith('.torrent'):
            continue
        if tor_hash_start and not tor_file.startswith(tor_hash_start):
            continue
        else:
            tor_file_path = os.path.join(tor_path, tor_file)
            tor_hash = tor_file.replace('.torrent', '')
            tor_magnet = get_magnet(tor_file_path)
            if not tor_magnet.startswith('magnet'):
                continue
            tor_name = get_name(tor_file_path)
            tor_info = get_info(tor_file_path)
            c.execute('''INSERT OR IGNORE INTO torrent(hash, name, magnet, info) VALUES (?, ?, ?, ?);''',
                    (tor_hash, tor_name, tor_magnet, tor_info))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print "python tor2db.py <tor_path> <db_path> [<tor_hash_start>]"
    else:
        tor_path = sys.argv[1]
        db_path = sys.argv[2]
        if len(sys.argv) > 3:
            tor_hash_start = sys.argv[3]
        else:
            tor_hash_start = None
        tor2db(tor_path, db_path, tor_hash_start)