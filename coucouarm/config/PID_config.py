import numpy as np

URDF_PATH = "/home/liu/coucouarm_v5/coucouarm_mujoco_for_github/coucouarm_v5_urdf/urdf/coucouarm_v5.urdf"
LOG_PATH = "/home/liu/coucouarm_v5/coucouarm_mujoco_for_github/data/csv/pid_control_log.csv"
N_JOINT = 6

DT = 0.002
RENDER_EVERY = 10

Kp = np.array([20, 135, 110, 7, 9, 0.01], dtype=float)
Ki = np.array([1, 3, 3, 3, 1, 1], dtype=float)
Kd = np.array([2.0, 1.5, 1.0, 0.15, 0.1, 0.001], dtype=float)
integral_limit = np.array([0.5, 0.5, 0.5, 0.5, 0.5, 0.5], dtype=float)

Q_INIT = np.array([0.0, 0.4, -0.4, 0.0, 0.0, 0.0], dtype=float)

TAU_LIMIT = np.array([10.0, 28.0, 27.0, 10.0, 10.0, 10.0], dtype=float)