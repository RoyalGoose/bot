def getflat(flat: int):
    if flat == 1:
        flat = 'Flat1'
    elif flat == 2:
        flat = 'Flat2'
    elif flat == 3:
        flat = 'Flat3'
    elif flat == 4:
        flat = 'Flat4'
    return flat


def getsquare(square: int):
    if square == 50:
        square = 'Sqr <= 50'
    if square == 100:
        square = 'Sqr BETWEEN 50 AND 100'
    if square == 200:
        square = 'Sqr BETWEEN 100 AND 200'
    if square == 201:
        square = 'Sqr >= 200'
    if square == 202:
        square = 'Any'
    return square


def getdist(dist):
    if dist == 'ЦАО':
        dist = "Dist like '%ЦАО%%'"
    if dist == 'САО':
        dist = "Dist like '%САО%%'"
    if dist == 'СВАО':
        dist = "Dist like '%СВАО%'"
    if dist == 'ВАО':
        dist = "Dist like '%ВАО%'"
    if dist == 'ЮВАО':
        dist = "Dist like '%ЮВАО%'"
    if dist == 'ЮАО':
        dist = "Dist like '%ЮАО%'"
    if dist == 'ЮЗАО':
        dist = "Dist like '%ЮЗАО%'"
    if dist == 'ЗАО':
        dist = "Dist like '%ЗАО%'"
    if dist == 'СЗАО':
        dist = "Dist like '%СЗАО%'"
    if dist == 'НАО':
        dist = "Dist like '%НАО (Новомосковский)%'"
    if dist == 'Any':
        dist = 'Any'
    return dist


def getprice(price: int):
    if price == 30:
        price = 'Price <= 30'
    if price == 40:
        price = 'Price BETWEEN 30 AND 50'
    if price == 75:
        price = 'Price BETWEEN 50 AND 100'
    if price == 100:
        price = 'Price >= 100'
    if price == 101:
        price = 'Any'
    return price
