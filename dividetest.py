import copy


def div(x, y):
    y_core = copy.deepcopy(y)
    a = 0
    while x >= y:
        R = 1
        y *= 2
        while x >= y:
            R *= 2
            y *= 2
        a += R
        x -= (y / 2)
        y = y_core
    print('reszta->' + str(x) + ';' + str(a) + '<-integer div')


div(6, 3)
