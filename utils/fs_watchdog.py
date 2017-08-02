import os
import sys
import time
import sqlite3
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

watch_path = sys.argv[1]
db_path = sys.argv[2]


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


class TorHandler(FileSystemEventHandler):
    def on_created(self, event):
        new_tor_name = os.path.basename(event.src_path)
        new_tor_hash = new_tor_name.split(".")[0]
        conn = sqlite3.connect(db_path)
        conn.text_factory = str
        c = conn.cursor()
        c.execute('SELECT * FROM torrent WHERE hash LIKE "' + new_tor_hash + '"')
        if len(c.fetchall()) == 0:
            print "Torrent: " + event.src_path + " not in db."
            new_tor_name = get_name(event.src_path)
            new_tor_magnet = get_magnet(event.src_path)
            new_tor_info = get_info(event.src_path)
            c.execute('''INSERT INTO torrent(hash, name, magnet, info) VALUES (?, ?, ?, ?);''',
                      (new_tor_hash, new_tor_name, new_tor_magnet, new_tor_info))
        conn.commit()


if __name__ == "__main__":
    event_handler = TorHandler()
    ob = Observer()
    ob.schedule(event_handler, path=watch_path, recursive=False)
    ob.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        ob.stop()
    ob.join()
