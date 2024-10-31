import numpy as np
import matplotlib.pyplot as plt
# 시간 설정

dt = 1.0

t = np.arange(0, 10, dt)
# 실제 위치 생성
actual_x = t
actual_y = t
# 측정값 생성
measurements_x = actual_x + np.random.normal(0, 1, size=len(t))
measurements_y = actual_y + np.random.normal(0, 1, size=len(t))
# 초기 상태와 공분산 행렬
x_est = np.array([0, 0])
P = np.eye(2)
# 상태 천이 행렬과 관측 행렬
A = np.eye(2)
H = np.eye(2)
# 프로세스 노이즈와 측정 노이즈 공분산
Q = np.eye(2) * 0.001
R = np.eye(2) * 1.0
x_estimates = []
for i in range(len(t)):
    z = np.array([measurements_x[i], measurements_y[i]])
    # 예측 단계
    x_pred = A @ x_est
    P_pred = A @ P @ A.T + Q
    # 업데이트 단계
    K = P_pred @ H.T @ np.linalg.inv(H @ P_pred @ H.T + R)
    x_est = x_pred + K @ (z - H @ x_pred)
    P = (np.eye(2) - K @ H) @ P_pred
    x_estimates.append(x_est.copy())
x_estimates = np.array(x_estimates)

# 결과 시각화
plt.plot(actual_x, actual_y, label='실제 경로')
plt.scatter(measurements_x, measurements_y, label='측정값', color='r', s=10)
plt.plot(x_estimates[:, 0], x_estimates[:, 1], label='추정된 경로', linestyle='--')
plt.legend()
plt.show()
