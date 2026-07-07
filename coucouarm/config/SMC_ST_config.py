import numpy as np


URDF_PATH = "/home/liu/coucouarm_v5/ros2_workspace/sim/coucouarm_v5_mujoco.urdf"
LOG_PATH = "/home/liu/coucouarm_v5/mujoco/data/csv/smc_st_log.csv"
N_JOINT = 6
DT = 0.002
RENDER_EVERY = 10

#SMC+ST
alpha = np.array([4.0, 4.0, 2.0, 2.0, 3.0, 1.0], dtype=float)
k1 = np.array([3.0, 3.0, 2.5, 1.5, 1.0, 1.0], dtype=float)
k2 = np.array([8.0, 8.0, 6.0, 4.0, 2.5, 2.0], dtype=float)
phi = np.array([0.03, 0.02, 0.01, 0.01, 0.01, 0.05], dtype=float)
Q_INIT = np.array([0.0, 0.4, -0.4, 0.0, 0.0, 0.0], dtype=float)
TAU_LIMIT = np.array([10.0, 28.0, 27.0, 10.0, 10.0, 10.0], dtype=float)