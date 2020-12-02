def getflat(rooms):
    if len(rooms) == 0:
        return 'Any'
    else:
        req = ''
        for i, j in enumerate(rooms):
            if j == -1: j = 0
            req += 'Room = {}'.format(j)
            if i + 1 < len(rooms):
                req += ' OR '
        return req


def getdist(dists):
    if dists == 'Any':
        return 'Any'
    else:
        req = ''
        for i, dist in enumerate(dists):
            req += "Underground LIKE '%{}%'".format(dist)
            if i + 1 < len(dists):
                req += ' OR '
        return req


def getreg(reg):
    if reg == 'Any':
        return 'Any'
    else:
        req = ''
        for i, j in enumerate(reg):
            req += "Underground LIKE '%{}%'".format(j)
            if i + 1 < len(reg):
                req += ' OR '
        return req


def getsquare(square):
    # min, max = square
    # if (min == 0 or min == -1 ) and (max == 0 or max == -1):
    #     return 'Any'
    # elif min == 0 or min == -1:
    #     return 'Area <= {}'.format(max)
    # elif max == 0 or max == -1:
    #     return 'Area >= {}'.format(min)
    # elif (min != 0 or min != -1) and (max != 0 or max != -1):
    #     return 'Area BETWEEN {} AND {}'.format(min, max)
    # else:
    #     print(min, max, 'else')
    mins, null = square
    if mins == 0 or mins == -1:
        return 'Any'
    else:
        return 'Area >= {}'.format(mins)


def getprice(price):
    min, max = price
    if (min == 0 or min == -1) and (max == 0 or max == -1):
        return 'Any'
    elif min == 0 or min == -1:
        return 'Price <= {}'.format(max)
    elif max == 0 or max == -1:
        return 'Price >= {}'.format(min)
    elif (min != 0 or min != -1 ) and (max != 0 or max != -1):
        return 'Price BETWEEN {} AND {}'.format(min, max)
    else:
        pass
