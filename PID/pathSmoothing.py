from copy import deepcopy
import matplotlib.pyplot as plt


def printpaths(path, newpath):
    for old, new in zip(path, newpath):
        print('[' + ', '.join('%.3f' % x for x in old) +
              '] -> [' + ', '.join('%.3f' % x for x in new) + ']')


path = [[0, 0],
        [0, 1],
        [0, 2],
        [1, 2],
        [2, 2],
        [3, 2],
        [4, 2],
        [4, 3],
        [4, 4]]


def smooth(path, weight_data=0.5, weight_smooth=0.1, tolerance=0.000001):

    newpath = deepcopy(path)

    change = tolerance

    while change >= tolerance:
        change = 0
        for i in range(1, len(path) - 1):
            for j in range(len(path[0])):
                d1 = weight_data*(path[i][j] - newpath[i][j])
                print(d1)
                d2 = weight_smooth * \
                    (newpath[i-1][j] + newpath[i+1][j] - 2*newpath[i][j])
                print(d2)
                change += abs(d1 + d2)
                newpath[i][j] += d1 + d2

    return newpath


printpaths(path, smooth(path))
# 원래 경로와 스무스한 경로를 출력
original_path = path
smooth_path = smooth(path)

# 그래프 그리기
plt.figure(figsize=(8, 6))

# 원래 경로를 점선으로 표시
original_x, original_y = zip(*original_path)
plt.plot(original_x, original_y, 'r--', label='Original Path')

# 스무스한 경로를 실선으로 표시
smooth_x, smooth_y = zip(*smooth_path)
plt.plot(smooth_x, smooth_y, 'b-', label='Smoothed Path')

# 시작과 끝 지점 표시
plt.scatter(*original_path[0], color='green', label='Start', zorder=5)
plt.scatter(*original_path[-1], color='purple', label='Goal', zorder=5)

# 레이블 추가
plt.title('Path Smoothing')
plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.legend()
plt.grid(True)

# 그래프 출력
plt.show()


# from copy import deepcopy
# import matplotlib.pyplot as plt
# import matplotlib.animation as animation


# # 경로 출력 함수
# def printpaths(path, newpath):
#     for old, new in zip(path, newpath):
#         print('[' + ', '.join('%.3f' % x for x in old) +
#               '] -> [' + ', '.join('%.3f' % x for x in new) + ']')


# path = [[0, 0],
#         [0, 1],
#         [0, 2],
#         [1, 2],
#         [2, 2],
#         [3, 2],
#         [4, 2],
#         [4, 3],
#         [4, 4]]


# # 스무스 함수 구현
# def smooth(path, weight_data=0.5, weight_smooth=0.1, tolerance=0.000001):
#     newpath = deepcopy(path)
#     change = tolerance

#     # 각 변화 단계 저장
#     steps = [deepcopy(newpath)]

#     while change >= tolerance:
#         change = 0
#         for i in range(1, len(path) - 1):
#             for j in range(len(path[0])):
#                 d1 = weight_data * (path[i][j] - newpath[i][j])
#                 d2 = weight_smooth * \
#                     (newpath[i-1][j] + newpath[i+1][j] - 2 * newpath[i][j])
#                 change += abs(d1 + d2)
#                 newpath[i][j] += d1 + d2
#         steps.append(deepcopy(newpath))  # 각 단계의 경로 저장

#     return steps


# # 경로 스무스 단계별 생성
# steps = smooth(path)

# # 그래프 애니메이션 생성
# fig, ax = plt.subplots(figsize=(8, 6))
# original_x, original_y = zip(*path)
# ax.plot(original_x, original_y, 'r--', label='Original Path', alpha=0.5)
# ax.scatter(*path[0], color='green', label='Start', zorder=5)
# ax.scatter(*path[-1], color='purple', label='Goal', zorder=5)
# line, = ax.plot([], [], 'b-', label='Smoothed Path')
# ax.legend()
# ax.grid(True)
# ax.set_title("Path Smoothing Animation")
# ax.set_xlabel("X-axis")
# ax.set_ylabel("Y-axis")

# # 애니메이션 초기화 함수


# def init():
#     line.set_data([], [])
#     return line,

# # 프레임 업데이트 함수


# def update(frame):
#     x, y = zip(*steps[frame])
#     line.set_data(x, y)
#     return line,


# # 애니메이션 설정
# ani = animation.FuncAnimation(fig, update, frames=len(
#     steps), init_func=init, blit=True, interval=200, repeat=False)

# plt.show()
