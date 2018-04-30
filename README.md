# BTSU

[![GitHub license](https://img.shields.io/badge/license-WTFPL-blue.svg)](https://raw.githubusercontent.com/peitaosu/BTSU/master/LICENSE)

## What is BTSU ?

BTSU is a torrent website project, powered by [p2pspider](https://github.com/fanpei91/p2pspider.git) and django.

## Step1: Get Torrents from DHT Network

1. Install Node.js

    ```
    sudo apt-get install nodejs nodejs-legacy npm -y
    ```

2. Install dependent packages

    ```
    cd p2pspider
    npm install -g

    # if encountered error - Cannot find module, please use:
    npm install
    ```

3. Install pm2 and run index.js with pm2 cluster mode

    ```
    sudo npm install pm2 -g
    cd p2pspider
    sudo pm2 start index.js -i 0
    ```

## Step2: Create Torrent Database with Torrents

All torrent files which get from DHT Network will be saved in `p2pspider/torrents`, need to use `transmission` to parse them and save `hash`, `name`, `magnet` and `info` into database.

1. Install transmission

    ```
    sudo apt-get install transmission-cli -y
    ```

2. Parse torrents and save to database

    ```
    # python utils/tor2db.py <torrents_folder> <database_path>

    python utils/tor2db.py p2pspider/torrents btsu/btsu/torrents.db
    ```

## Step3: Setup your BTSU

BTSU is a django project, please:

1. install Django

    ```
    pip install Django

    # or install from requirements.txt

    pip install -r requirements.txt
    ```

2. update the `TOR_DB_PATH` and add your server ip into `ALLOWED_HOSTS` in `btsu/btsu/settings.py` before you run the server.

    ```
    # python {your_code_path}/btsu/manage.py runserver 0.0.0.0:{your_port}

    python btsu/btsu/manage.py runserver 0.0.0.0:1234
    ```

## Step4: Keep BTSU Running

```keep_running.sh``` is a script which can keep the BTSU running and restart it when the server down.

Please update the `{your_code_path}` inside before you use it.

## Step5: Watch New Torrent and Update Database

```fs_watchdog.py``` is a script which can watch torrents folder and update database while get new torrent. You need to install watchdog before use it.

```
pip install watchdog

# or install from requirements.txt

pip install -r requirements.txt

# then

python fs_watchdog.py <torrent_folder> <database>
```