#!/bin/bash

if ! lsof -i:{your_port}
then
    nohup python {your_code_path}/btsu/manage.py runserver 0.0.0.0:{your_port} &
fi
