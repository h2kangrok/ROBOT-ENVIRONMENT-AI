# def sense(p, measurement, colors, sensor_right):
#     a = []
#     for i in range(len(p)):
#         q = []
#         for j in range(len(p[0])):
#             hit = (measurement == colors[i][j])
#             q.append(p[i][j] * (hit * sensor_right +
#                      (1-hit) * (1-sensor_right)))
#         a.append(q)
#     si = sum(sum(a, []))
#     for i in range(len(a)):
#         for j in range(len(a[0])):
#             a[i][j] = a[i][j] / si
#     return a
def sense(p, measurement, colors, sensor_right):
    a = []
    for i in range(len(p)):
        q = []
        for j in range(len(p[0])):
            hit = (measurement == colors[i][j])
            q.append(p[i][j] * (hit * sensor_right +
                                (1-hit) * (1-sensor_right)))
        a.append(q)
    si = sum(sum(a, []))
    if si == 0:
        return p  # Return the previous distribution if no match found
    for i in range(len(a)):
        for j in range(len(a[0])):
            a[i][j] = a[i][j] / si
    return a


def move(p, motion, p_move):
    dy = motion[0]
    dx = motion[1]
    b = [[0.0 for row in range(len(p[0]))] for col in range(len(p))]
    for i in range(len(p)):
        for j in range(len(p[0])):
            s = p_move * (p[(i-dy) % len(p)][(j-dx) % len(p[i])])
            s = s + (1-p_move) * p[i][j]
    return b


def localize(colors, measurements, motions, sensor_right, p_move):
    pinit = 1.0 / float(len(colors)) / float(len(colors[0]))
    p = [[pinit for row in range(len(colors[0]))]
         for col in range(len(colors))]
    for k in range(len(measurements)):
        p = move(p, motions[k], p_move)
        p = sense(p, measurements[k], colors, sensor_right)
    return p


def show(p):
    rows = [
        '[' + ','.join(map(lambda x: '{0:.5f}'.format(x), r)) + ']' for r in p]
    print('[' + ',\n '.join(rows) + ']')

# test1


colors = [['G', 'G', 'G'],
          ['G', 'G', 'G'],
          ['G', 'G', 'G']]

measurements = ['R']
motions = [[0, 0]]
sensor_right = 1.0
p_move = 1.0
p = localize(colors, measurements, motions, sensor_right, p_move)
show(p)
