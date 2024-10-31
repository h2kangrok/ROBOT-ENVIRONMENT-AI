import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import heapq

# 그리드 설정 (1: 장애물 추가)
grid = np.array([
    [0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 0],
    [0, 1, 0, 0, 1, 0],
    [0, 1, 0, 1, 1, 0],
    [0, 0, 0, 0, 0, 0]
])
# 시작 지점과 목표 지점 설정
start = (0, 0)
goal = (4, 5)
# 이동 방향 설정 (대각선 포함)
delta = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]


def heuristic(a, b):
    # 대각선 거리 사용
    dx = abs(a[0] - b[0])
    dy = abs(a[1] - b[1])
    return max(dx, dy)


def astar(grid, start, goal):
    open_list = []
    heapq.heappush(open_list, (heuristic(start, goal), 0, start, [start]))
    visited = set()
    visited.add(start)
    print(visited)
    visited_nodes = []

    while open_list:
        estimated_total, cost_so_far, current, path = heapq.heappop(open_list)
        # print(estimated_total)
        visited_nodes.append(current)
        # print(visited_nodes)

        if current == goal:
            return path, visited_nodes

        for dx, dy in delta:
            neighbor = (current[0] + dx, current[1] + dy)
            print(neighbor)
            if (0 <= neighbor[0] < grid.shape[0] and
                0 <= neighbor[1] < grid.shape[1] and
                grid[neighbor[0]][neighbor[1]] == 0 and
                    neighbor not in visited):

                visited.add(neighbor)

                cost = np.sqrt(dx**2 + dy**2)
                total_cost = cost_so_far + cost
                estimated_total = total_cost + heuristic(neighbor, goal)
                heapq.heappush(open_list, (estimated_total,
                               total_cost, neighbor, path + [neighbor]))

    return None, visited_nodes


# A* 알고리즘 실행
optimal_path, visited_nodes = astar(grid, start, goal)
# 시각화
fig, ax = plt.subplots()
ax.set_title('대각선 이동을 허용하는 A* 경로 탐색')


def update(num):
    ax.clear()
    ax.imshow(grid, cmap='Greys')
    # 장애물 표시

    obstacles = np.argwhere(grid == 1)
    if obstacles.size > 0:
        x_obs, y_obs = zip(*obstacles)
        ax.plot(y_obs, x_obs, 's', color='black', markersize=10)
    # 방문한 노드 표시
    x_vals, y_vals = zip(*visited_nodes[:num+1])
    ax.plot(y_vals, x_vals, 'o', color='yellow', markersize=5)

    # 최적 경로 표시
    if optimal_path and num >= len(visited_nodes) - 1:
        x_opt, y_opt = zip(*optimal_path)
        ax.plot(y_opt, x_opt, color='blue', linewidth=2)

        # 시작 지점과 목표 지점 표시
        # 시작 지점과 목표 지점 표시
        ax.plot(start[1], start[0], 's', color='green',
                markersize=10, label='시작')
        ax.plot(goal[1], goal[0], 's', color='red', markersize=10, label='목표')

        ax.legend()
        ax.set_xticks([])
        ax.set_yticks([])


ani = animation.FuncAnimation(fig, update, frames=len(
    visited_nodes)+20, interval=200, repeat=False)

plt.show()
