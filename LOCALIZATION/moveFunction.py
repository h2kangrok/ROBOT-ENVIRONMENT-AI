p = [0, 1, 0, 0, 0]


def move(p, U):
    U = U % len(p)
    q = p[-U:] + p[:-U]
    return q


print(move(p, 1))
