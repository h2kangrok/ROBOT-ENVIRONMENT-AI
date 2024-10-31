# ----------
# 다음을 반환하는optim_policy 함수를 작성합니다.
# 로봇에 대한 최적의 정책을 보여주는 그리드
# 모션. 이는 최적의 조건이 있어야 함을 의미합니다.

# 탐색 가능한 각 셀과 연관된 방향
# 목표는 달성할 수 있다.
#
# 탐색할 수 없는 셀뿐만 아니라
# 목표에 도달할 수 없는 경우 문자열이 있어야 합니다.
# 다음과 같이 단일 공백(' ')을 포함합니다.
# 목표 셀에는 '*'가 있어야 합니다.
# ----------
grid = [[0, 1, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0]]
init = [0, 0]
goal = [len(grid)-1, len(grid[0])-1]
cost = 1  # the cost associated with moving from a cell to an adjacent one
delta = [[-1, 0],  # go up
         [0, -1],  # go left
         [1, 0],  # go down
         [0, 1]]  # go right
delta_name = ['^', '<', 'v', '>']


def optimum_policy(grid, goal, cost):
    value = [[99 for row in range(len(grid[0]))] for col in range(len(grid))]
    print(value)
    policy = [[' ' for row in range(len(grid[0]))] for col in range(len(grid))]
    print(policy)
    policy[len(grid) - 1][len(grid[0]) - 1] = '*'
    print(policy)
    change = True

    while change:
        change = False
        for x in range(len(grid)):
            for y in range(len(grid[0])):
                if goal[0] == x and goal[1] == y:
                    if value[x][y] > 0:
                        value[x][y] = 0
                        change = True

                elif grid[x][y] == 0:
                    for a in range(len(delta)):
                        x2 = x + delta[a][0]
                        y2 = y + delta[a][1]
                        if x2 >= 0 and x2 < len(grid) and y2 >= 0 and y2 < len(grid[0]) and grid[x2][y2] == 0:
                            v2 = value[x2][y2] + cost
                            if v2 < value[x][y]:
                                change = True
                                value[x][y] = v2
                                policy[x][y] = delta_name[a]
    return policy


print(optimum_policy(grid, goal, cost))
