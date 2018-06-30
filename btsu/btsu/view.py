from django.http import HttpResponse
from django.shortcuts import render
from django.conf import settings
import os
import sys
import subprocess
import json
import StringIO
import mimetypes
import sqlite3
from sqlite3 import OperationalError

mimetypes.init()



def response_console_output(func):
    def new_func(*args, **kwargs):
        console_output = StringIO.StringIO()
        sys.stdout = console_output
        func(*args, **kwargs)
        sys.stdout = sys.__stdout__
        return HttpResponse(['<BR>' if char == '\n' else char for char in console_output.getvalue()])
    return new_func


@response_console_output
def info(request):
    print 'Hello BTSU!'


def get_console_output(command):
    return subprocess.Popen(command, stdout=subprocess.PIPE, shell=True).communicate()[0]


def tor(request):
    request.encoding = 'utf-8'
    if 'hash' in request.GET:
        conn = sqlite3.connect(settings.TOR_DB_PATH)
        c = conn.cursor()
        c.execute("SELECT info FROM torrent WHERE hash = '" +
                  request.GET['hash'] + "'")
        tor_info = c.fetchone()[0]
        return HttpResponse(['<BR>'.join(tor_info.split('\n'))])


def list(request):
    context = {}
    request.encoding = 'utf-8'
    if 'q' in request.GET:
        conn = sqlite3.connect(settings.TOR_DB_PATH)
        c = conn.cursor()
        try:
            c.execute("SELECT * FROM torrent WHERE hash LIKE '" +
                    request.GET['q'] + "%'")
            context['query_result'] = []
            for row in c.fetchall():
                context['query_result'].append(row)
            context['in_maintenance'] = False
        except OperationalError:
            context['in_maintenance'] = True
        return render(request, 'list.html', context)


def index(request):
    context = {}
    conn = sqlite3.connect(settings.TOR_DB_PATH)
    c = conn.cursor()
    try:
        c.execute("SELECT MAX(_ROWID_) FROM torrent LIMIT 1")
        context['total'] = c.fetchone()[0]
        context['in_maintenance'] = False
    except OperationalError:
        context['in_maintenance'] = True
    return render(request, 'index.html', context)


def all(request):
    context = {}
    context['list'] = []
    for i in range(255):
        context['list'].append('%0.2X' % i)
    return render(request, 'all.html', context)


def search(request):
    context = {}
    if 's' in request.GET:
        conn = sqlite3.connect(settings.TOR_DB_PATH)
        c = conn.cursor()
        try:
            c.execute("SELECT * FROM torrent WHERE name LIKE '%" +
                    request.GET['s'] + "%'")
            context['search_result'] = []
            for row in c.fetchall():
                if len(row[1]) > 80:
                    row = (row[0], row[1][0:77] + '...', row[2], row[3])
                context['search_result'].append(row)
            context['search_count'] = len(context['search_result'])
            context['in_maintenance'] = False
        except OperationalError:
            context['in_maintenance'] = True
        return render(request, 'search.html', context)

def down(request):
    context= {}
    if settings.TRANSMISSION_USER == '' or settings.TRANSMISSION_PWD == '' or settings.TRANSMISSION_WEB == '':
        context['not_set'] = True
    else: 
        context['hash'] = request.GET['hash']
        context['webui'] = settings.TRANSMISSION_WEB
        command = 'transmission-remote -a "magnet:?xt=urn:btih:{}" -n "{}:{}"'.format(context['hash'], settings.TRANSMISSION_USER, settings.TRANSMISSION_PWD)
        result = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True).communicate()[0]
        if "success" in result:
            context['add_success'] = True
        else:
            context['add_success'] = False
            context['error'] = result
    return render(request, 'down.html', context)

def play(request):
    context = {}
    conn = sqlite3.connect(settings.TOR_DB_PATH)
    c = conn.cursor()
    try:
        c.execute("SELECT MAX(_ROWID_) FROM torrent LIMIT 1")
        context['in_maintenance'] = False
    except OperationalError:
        context['in_maintenance'] = True
    if 'hash' in request.GET:
        context['hash'] = request.GET['hash']
    return render(request, 'play.html', context)
