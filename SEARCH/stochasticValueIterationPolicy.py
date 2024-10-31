# stochastic_value라는 함수를 작성합니다.
# 두 개의 그리드를 반환합니다. 첫 번째 그리드인 값은 다음과 같아야 합니다.
# 표시된 대로 각 셀의 계산된 값을 포함합니다.
# 각 셀에 대한 최적의 정책을 포함합니다.

delta = [[-1, 0],  # go up
         [0, -1],  # go left
         [1, 0],  # go down
         [0, 1]]  # go right

delta_name = ['^', '<', 'v', '>']


def stochastic_value(grid, goal, cost_step, collision_cost, success_prob):
    # Probability(stepping left) = prob(stepping right) = failure_prob
    failure_prob = (1.0 - success_prob)/2.0
    value = [[collision_cost for col in range(
        len(grid[0]))] for row in range(len(grid))]
    policy = [[' ' for col in range(len(grid[0]))] for row in range(len(grid))]

    change = True
    while change == True:
        change = False
        for x in range(len(grid)):
            for y in range(len(grid[0])):
                if [x, y] == goal:
                    if value[x][y] > 0:
                        value[x][y] = 0
                        change = True
                elif grid[x][y] == 0:
                    for a in range(len(delta)):

                        v2 = cost_step

                        # explore outcomes
                        for i in range(-1, 2):
                            a2 = (a+i) % len(delta)
                            x2 = x + delta[a2][0]
                            y2 = y + delta[a2][1]

                            if i == 0:
                                prob = success_prob
                            else:
                                prob = failure_prob

                            if x2 >= 0 and x2 < len(grid) and y2 >= 0 and y2 < len(grid[0]) and grid[x2][y2] == 0:
                                v2 += prob*value[x2][y2]
                            else:
                                v2 += prob*collision_cost

                        if v2 < value[x][y]:
                            print("original :",
                                  value[x][y], "changed :", v2)
                            value[x][y] = v2
                            policy[x][y] = delta_name[a]
                            change = True
    # print policy
    return value, policy


grid = [[0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 1, 1, 0]]
goal = [0, len(grid[0])-1]  # Goal is in top right corner
cost_step = 1
collision_cost = 100
success_prob = 0.5

value, policy = stochastic_value(
    grid, goal, cost_step, collision_cost, success_prob)

for row in value:
    print(row)
for row in policy:
    print(row)
