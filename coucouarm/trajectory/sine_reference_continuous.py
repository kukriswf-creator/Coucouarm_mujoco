import numpy as np
from coucouarm.config import PID_config as cfg


class SineReference:
    def __init__(self):
        self.q_base = cfg.Q_INIT.copy()
        self.amp = np.array([0.7, 0.2, 0.2, 0.6, 0.5, 0.5], dtype=float)
        self.omega = np.array([0.5, 0.5, 0.5, 0.4, 0.4, 0.4], dtype=float)


    def get(self, t: float):
       
        qd = self.q_base + self.amp * np.sin(self.omega * t)
        dqd = self.amp * self.omega * np.cos(self.omega * t)
        ddqd = -self.amp * (self.omega ** 2) * np.sin(self.omega * t)


        return qd, dqd, ddqd