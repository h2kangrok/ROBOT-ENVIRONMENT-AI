# 20x20 크기의 큰 그리드를 생성하고, 무작위로 장애물을 배치합니다. A*
# 알고리즘은 복잡한 환경에서 최적 경로를 찾으며, 애니메이션을 통해 탐색
# 과정을 시각화합니다.

import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import heapq

# 큰 그리드 생성 (20x20)
np.random.seed(0)
grid_size = (20, 20)
grid = np.zeros(grid_size)
obstacle_probability = 0.2

for i in range(grid_size[0]):
    for j in range(grid_size[1]):
        if np.random.rand() < obstacle_probability:
            grid[i][j] = 1

grid[0][0] = 0  # 시작 지점은 빈 공간으로 설정
grid[grid_size[0]-1][grid_size[1]-1] = 0  # 목표 지점은 빈 공간으로 설정

# 시작 지점과 목표 지점 설정
start = (0, 0)
goal = (grid_size[0]-1, grid_size[1]-1)

# 이동 방향 설정 (상, 하, 좌, 우)
delta = [(-1, 0), (1, 0), (0, -1), (0, 1)]


def heuristic(a, b):
    # 맨해튼 거리 사용
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def astar(grid, start, goal):
    open_list = []
    heapq.heappush(open_list, (heuristic(start, goal), 0, start, [start]))
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

            if (0 <= neighbor[0] < grid_size[0] and 0 <= neighbor[1] < grid_size[1] and grid[neighbor[0]][neighbor[1]] == 0 and neighbor not in visited):
                visited.add(neighbor)
                total_cost = cost_so_far + 1
                estimated_total = total_cost + heuristic(neighbor, goal)
                heapq.heappush(open_list, (estimated_total,
                               total_cost, neighbor, path + [neighbor]))
    return None, visited_nodes


# A* 알고리즘 실행
optimal_path, visited_nodes = astar(grid, start, goal)
print(visited_nodes)
print(astar(grid, start, goal))
# 시각화
fig, ax = plt.subplots(figsize=(10, 10))

ax.set_title('큰 그리드에서 A* 경로 탐색')


def update(num):
    ax.clear()
    ax.imshow(grid, cmap='Greys')

    # 장애물 표시
    obstacles = np.argwhere(grid == 1)
    if obstacles.size > 0:
        x_obs, y_obs = zip(*obstacles)
        ax.plot(y_obs, x_obs, 's', color='black', markersize=4)

    # 방문한 노드 표시
    x_vals, y_vals = zip(*visited_nodes[:num+1])
    ax.plot(y_vals, x_vals, 'o', color='yellow', markersize=2)

    # 최적 경로 표시
    if optimal_path and num >= len(visited_nodes) - 1:
        x_opt, y_opt = zip(*optimal_path)
        ax.plot(y_opt, x_opt, color='blue', linewidth=2)

    # 시작 지점과 목표 지점 표시
    ax.plot(start[1], start[0], 's', color='green', markersize=8, label='시작')

    ax.plot(goal[1], goal[0], 's', color='red', markersize=8, label='목표')

    ax.legend()
    ax.set_xticks([])
    ax.set_yticks([])


ani = animation.FuncAnimation(fig, update, frames=len(
    visited_nodes)+50, interval=50, repeat=False)

plt.show()
