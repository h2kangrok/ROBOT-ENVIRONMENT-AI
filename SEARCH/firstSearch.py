# ----------
# Problem:
#
# 목록을 반환하는 함수 search()를 정의합니다.
# [최적 경로 길이, 행, 열] 형식입니다. 을 위한
# 아래 표시된 그리드에서 함수는 출력되어야 합니다.
# [11, 4, 5].
#
# 시작점에서 유효한 경로가 없는 경우
# 목표에 도달하려면 함수가 문자열을 반환해야합니다.
# 'fail'
# ----------
# Grid format:
# 0 = Navigable space
# 1 = Occupied space

grid = [[0, 0, 1, 0, 0, 0], [0, 0, 1, 0, 0, 0], [
    0, 0, 0, 0, 1, 0], [0, 0, 1, 1, 1, 0], [0, 0, 0, 0, 1, 0]]
init = [0, 0]
goal = [len(grid)-1, len(grid[0])-1]
cost = 1
delta = [[-1, 0],  # go up
         [0, -1],
         [1, 0],
         [0, 1]]

delta_name = ['^', '<', 'v', '>']


def find_min_state(open_list, visited):
    # print visited
    if open_list == []:
        return "fail"
    min = 0
    for _ in range(len(open_list)):
        if ([open_list[min][1], open_list[min][2]] not in visited):
            if (open_list[_][0] < open_list[min][0]):
                min = _
            else:
                min += 1
            if min >= len(open_list):
                min -= 1
                break
        # print grid[0]
        # print open_list
        # print "min", min
    return open_list[min]


def expand(state, delta, visited, open_list):
    # print "open_list_before: ",open_list
    for _ in range(4):
        if ([state[1] + delta[_][0], state[2] + delta[_][1]] not in visited):
            if (state[1] + delta[_][0] >= 0 and state[2] + delta[_][1] >= 0) and (state[1] + delta[_][0] <= (len(grid)-1) and state[2] + delta[_][1] <= (len(grid[0])-1)) and (grid[state[1] + delta[_][0]][state[2] + delta[_][1]] != 1):
                # print "visited :", [state[1] + delta[_][0], state[2], delta[_][1]]
                visited.append(
                    [state[1] + delta[_][0], state[2] + delta[_][1]])
                open_list.append(
                    [state[0] + 1, state[1] + delta[_][0], state[2] + delta[_][1]])
    # print "open_list_after: ",open_list
    return open_list


def search(grid, init, goal, cost):
    visited = []
    open_list = []
    path = None
    visited.append([0, 0])
    init.append(0)
    # open_list.append(init)
    g = 0
    next_state = init
    # print open_list

    for g in range(len(grid)*len(grid[0])):
        open_list = (expand(next_state, delta, visited, open_list))
        # print open_list
        # print visited
        next_state = find_min_state(open_list, visited)
        if next_state == "fail":
            break

        open_list.remove(next_state)
        # print next_state
        # print open_list
        if [next_state[1], next_state[2]] == goal:
            # print "Successful to reach the goal"
            # path = [g, next_state[1], next_state[2]]
            path = next_state
            # print path
            print(next_state)
            break

        # print visited
    if path == None:
        print("fail")


search(grid, init, goal, cost)
