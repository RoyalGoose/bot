import telebot
from telebot import types
from telebot import apihelper
from telebot.types import Message

from const import TOKEN
from const import PROXY

import csv

bot = telebot.TeleBot(token=TOKEN, threaded=False)
apihelper.proxy = {'https': PROXY}


def changerooms(r1, r2, r3, r4):
    rooms = []
    if r1 == -1:
        rooms.append(0)
    if r1 and r1 != -1:
        rooms.append(1)
    if r2:
        rooms.append(2)
    if r3:
        rooms.append(3)
    if r4:
        rooms.append(4)
    if len(rooms) == 0:
        return []
    return rooms


def changedist(vco, tco, tt, ztk):
    path = 'metro.csv'
    f = open(path, encoding='UTF-8')
    reader = csv.reader(f, delimiter=';')
    kcv = ['кольцо']
    toc = ['3кольца']
    ttk = ['ттк']
    pst = ['зттк']
    for i, row in enumerate(reader):
        if i > 1:
            if row[0] != '':
                kcv.append(row[0].lower().capitalize())
                toc.append(row[0].lower().capitalize())
                ttk.append(row[0].lower().capitalize())
                pst.append(row[0].lower().capitalize())
            if row[2] != '':
                toc.append(row[2].lower().capitalize())
                ttk.append(row[2].lower().capitalize())
                pst.append(row[2].lower().capitalize())
            if row[4] != '':
                ttk.append(row[4].lower().capitalize())
                pst.append(row[4].lower().capitalize())
            if row[6] != '':
                pst.append(row[6].lower().capitalize())
    if vco:
        return kcv
    elif tco:
        return toc
    elif tt:
        return ttk
    elif ztk:
        return pst
    else:
        return 'Any'


def changereg(cao, sao, svao, vao, uvao, uao, uzao, zao, szao, nao):
    path = 'metro_mapping.csv'
    f = open(path)
    reader = csv.reader(f, delimiter=';')
    dist = []
    if cao:
        dist.append('Центральный административный округ')
    if sao:
        dist.append('Северный административный округ')
    if svao:
        dist.append('Северо-Восточный административный округ')
    if vao:
        dist.append('Восточный административный округ')
    if uvao:
        dist.append('Юго-Восточный административный округ')
    if uao:
        dist.append('Южный административный округ')
    if uzao:
        dist.append('Юго-Западный административный округ')
    if zao:
        dist.append('Западный административный округ')
    if szao:
        dist.append('Северо-Западный административный округ')
    if nao:
        dist.append('Новомосковский административный округ')
    if len(dist) == 0:
        return 'Any'
    reg = []
    for row in reader:
        if row[2] in dist:
            reg.append(row[0])
    return reg


'''
def changesqure(min, max):
    if (min == 0) & (max == 0):
        return 'Any'
    else:
        return min, max

def changeprice(min, max):
    return min, max
'''
