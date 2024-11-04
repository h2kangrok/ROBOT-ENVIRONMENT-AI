# p = [0.2, 0.2, 0.2, 0.2, 0.2]
# world = ['green', 'red', 'red', 'green', 'green']
# Z = 'red'
# pHit = 0.6
# pMiss = 0.2


# def sense(p, Z):
#     q = []
#     sum = 0
#     for i in range(len(p)):
#         hit = (Z == world[i])
#         q.append(p[i] * (hit * pHit + (1-hit) * pMiss))
#         sum += q[i]
#     print(q)

#     q = [x/sum for x in q]
#     return q


# print(sum)
# print(sense(p, Z))


p = [0.2, 0.2, 0.2, 0.2, 0.2]
world = ['green', 'red', 'red', 'green', 'green']
Z = 'red'
pHit = 0.6
pMiss = 0.2


def sense(p, Z):
    q = []
    sum = 0
    for i in range(len(p)):
        hit = (Z == world[i])
        q.append(p[i] * (hit * pHit + (1-hit) * pMiss))
        sum += q[i]
    print(sum)
    for i in range(len(p)):
        q[i] = q[i]/sum
    return q


print(sense(p, Z))
