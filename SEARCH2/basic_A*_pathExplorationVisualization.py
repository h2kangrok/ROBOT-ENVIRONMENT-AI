import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import heapq

# 그리드 설정 (0: 이동 가능, 1: 장애물)

grid = np.zeros((5, 6))

# 시작 지점과 목표 지점 설정

start = (0, 0)

goal = (4, 5)

# 이동 방향 설정 (상, 하, 좌, 우)

delta = [(-1, 0), (1, 0), (0, -1), (0, 1)]


def heuristic(a, b):

    # 맨해튼 거리 사용

    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def astar(grid, start, goal):

    open_list = []

    heapq.heappush(open_list, (0 + heuristic(start, goal), 0, start, [start]))

    visited = set()

    visited.add(start)

    visited_nodes = []

    while open_list:

        estimated_total, cost_so_far, current, path = heapq.heappop(open_list)

        visited_nodes.append(current)

        if current == goal:
            return path, visited_nodes

        for dx, dy in delta:
            neighbor = (current[0] + dx, current[1] + dy)

            if (0 <= neighbor[0] < grid.shape[0] and 0 <= neighbor[1] < grid.shape[1] and grid[neighbor[0]][neighbor[1]] == 0 and neighbor not in visited):
                visited.add(neighbor)
                total_cost = cost_so_far + 1
                estimated_total = total_cost + heuristic(neighbor, goal)
                heapq.heappush(open_list, (estimated_total,
                               total_cost, neighbor, path + [neighbor]))

    return None, visited_nodes


# A* 알고리즘 실행
optimal_path, visited_nodes = astar(grid, start, goal)

# 시각화
fig, ax = plt.subplots()
ax.set_title('A* 경로 탐색 시각화')


def update(num):

    ax.clear()
    ax.imshow(grid, cmap='Greys')

    # 방문한 노드 표시
    x_vals, y_vals = zip(*visited_nodes[:num+1])
    ax.plot(y_vals, x_vals, 'o', color='yellow', markersize=5)

    # 최적 경로 표시

    if optimal_path and num >= len(visited_nodes) - 1:
        x_opt, y_opt = zip(*optimal_path)
        ax.plot(y_opt, x_opt, color='blue', linewidth=2)

    # 시작 지점과 목표 지점 표시

    ax.plot(start[1], start[0], 's', color='green', markersize=10, label='시작')
    ax.plot(goal[1], goal[0], 's', color='red', markersize=10, label='목표')

    ax.legend()
    ax.set_xticks([])
    ax.set_yticks([])


ani = animation.FuncAnimation(fig, update, frames=len(
    visited_nodes)+10, interval=200, repeat=False)

plt.show()
