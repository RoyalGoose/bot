def getflat(flat: int):
    if flat == 1:
        flat = '1'
    elif flat == 2:
        flat = '2х'
    elif flat == 3:
        flat = '3х'
    elif flat == 4:
        flat = '4х'
    elif flat == 'Any':
        flat = False
    return flat


def getsquare(square: int):
    if square == 50:
        square = ' площадью менее 50 м²'
    if square == 100:
        square = ' площадью 50-100 м²'
    if square == 200:
        square = ' площадью 100-200 м²'
    if square == 201:
        square = ' площадью более 200 м²'
    if square == 202:
        square = ' с любой площадью'
    return square


def getdist(vco, tco, ttk, ztk):
    if vco:
        return 'в пределах кольцевой'
    elif tco:
        return 'в пределах 3 станций от кольца'
    elif ttk:
        return 'в пределах ТТК'
    elif ztk:
        return 'в пределах 5 станций от кольца'
    else:
        return 'в любом районе'


def getprice(price: int):
    if price == 30:
        price = ' за цену в менее 30 тыс. руб/месяц'
    if price == 40:
        price = ' за 30-50 тыс. руб/месяц'
    if price == 75:
        price = ' за 50-100 тыс. руб/месяц'
    if price == 100:
        price = ' за цену в более 100 тыс. руб'
    if price == 101:
        price = ' и с любой ценой'
    return price


def roomtext(r1, r2, r3, r4):
    txt = ''
    i = 0
    if r1:
        txt += '1'
        i += 1
    if r2:
        if i > 0:
            txt += ', 2'
        else:
            txt += '2'
        i += 1
    if r3:
        if i > 0:
            txt += ', 3'
        else:
            txt += '3'
        i += 1
    if r4:
        if i > 0:
            txt += ', 4 и более'
        else:
            txt += '4'
        i += 1
    if not r1 and not r2 and not r3 and not r4:
        return 'любое количество комнат'
    if r1 and i == 1:
        txt += ' комната'
    elif (r2 or r3) and i >= 1:
        txt += ' комнаты'
    else:
        txt += ' комнат'
    return txt


import message_handler as mh


def regtext(cao, sao, svao, vao, uvao, uao, uzao, zao, szao, nao):
    txt = ''
    if cao:
        txt += 'ЦАО, '
    if sao:
        txt += 'САО, '
    if svao:
        txt += 'СВАО, '
    if vao:
        txt += 'ВАО, '
    if uvao:
        txt += 'ЮВАО, '
    if uao:
        txt += 'ЮАО, '
    if uzao:
        txt += 'ЮЗАО, '
    if zao:
        txt += 'ЗАО, '
    if szao:
        txt += 'СЗАО, '
    if nao:
        txt += 'НАО (Новомосковский)'
    if not cao and not sao and not svao and not vao and not uvao and not uao and not uzao and not zao and not szao and not nao:
        return 'любой округ'
    return txt[:-2]


def sqtext(min):
    if min != -1 and min != 0:
        return 'минимальная площадь %s м²' % min
    else:
        return 'любая площадь'


def pricetext(min):
    if min != -1 and min != 0:
        return 'минимальная цена %s руб.' % min
    else:
        return 'любая цена'


def ffilter(r1, r2, r3, r4,
            vco, tco, ttk, ztk,
            cao,sao, svao, vao, uvao, uao, uzao, zao, szao, nao,
            minsq, minp):
    f = roomtext(r1, r2, r3, r4)
    d = getdist(vco, tco, ttk, ztk)
    r = regtext(cao, sao, svao, vao, uvao, uao, uzao, zao, szao, nao)
    s = sqtext(minsq)
    p = pricetext(minp)
    return "Ваш фильтр: " + f + ', ' + d + ', ' + r + ', ' + s + ', ' + p
