import numpy as np
import matplotlib.pyplot as plt
# 시간 설정
dt = 1.0
t = np.arange(0, 10, dt)
# 실제 속도와 측정값 생성
actual_velocity = 2 * t  # 가속도 2 m/s^2
measurements = actual_velocity + np.random.normal(0, 2, size=len(t))
# 초기 추정값과 불확실성 설정
v_est = 0.0
P = 1.0
# 상태 천이 행렬과 관측 행렬
A = 1.0
H = 1.0
# 프로세스 노이즈와 측정 노이즈 공분산
Q = 0.1
R = 4.0

v_estimates = []
for z in measurements:
    # 예측 단계
    v_pred = A * v_est
    P_pred = A * P * A + Q
    # 업데이트 단계
    K = P_pred * H / (H * P_pred * H + R)
    v_est = v_pred + K * (z - H * v_pred)
    P = (1 - K * H) * P_pred
    v_estimates.append(v_est)
# 결과 시각화
plt.plot(t, actual_velocity, label='actual_velocity')
plt.plot(t, measurements, label='measurements', linestyle='dotted')
plt.plot(t, v_estimates, label='v_estimates', linestyle='--')
plt.legend()
plt.show()
