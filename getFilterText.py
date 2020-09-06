def getflat(flat: int):
    if flat == 1:
        flat = '1'
    elif flat == 2:
        flat = '2х'
    elif flat == 3:
        flat = '3х'
    elif flat == 4:
        flat = '4х'
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


def getdist(dist):
    if dist == 'Any':
        dist = 'любом районе'
    return dist


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
