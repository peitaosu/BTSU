import os
import sys
import time
import sqlite3
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

watch_path = sys.argv[1]
db_path = sys.argv[2]
tors = []

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

def write_db():
    conn = sqlite3.connect(db_path)
    conn.text_factory = str
    c = conn.cursor()
    for tor in tors:
        c.execute('''INSERT OR IGNORE INTO torrent(hash, name, magnet, info) VALUES (?, ?, ?, ?);''', (tor['hash'], tor['name'], tor['magnet'], tor['info']))
    conn.commit()
    conn.close()


class TorHandler(FileSystemEventHandler):
    def on_created(self, event):
        new_tor_name = os.path.basename(event.src_path)
        if not new_tor_name.endswith('.torrent'):
            return
        new_tor_hash = new_tor_name.split(".")[0]
        new_tor_magnet = get_magnet(event.src_path)
        if not new_tor_magnet.startswith('magnet'):
            return
        new_tor_name = get_name(event.src_path)
        new_tor_info = get_info(event.src_path)
        tors.append(
            {
                "hash": new_tor_hash,
                "name": new_tor_name,
                "magnet": new_tor_magnet,
                "info": new_tor_info
            }
        )

if __name__ == "__main__":
    event_handler = TorHandler()
    ob = Observer()
    ob.schedule(event_handler, path=watch_path, recursive=False)
    ob.start()

    try:
        while True:
            time.sleep(1)
    finally:
        ob.stop()
        write_db()
    ob.join()
