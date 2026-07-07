import numpy as np
from coucouarm.config import PID_config as PIDcfg

class PIDController:
    def __init__(self, reference):
        self.reference = reference
        self.integral_e = np.zeros(PIDcfg.N_JOINT)

    def tau_pid(self, t, q, dq, dt):

        qd, dqd, ddqd = self.reference.get(t)
        
        e = qd - q
        de = dqd - dq
        self.Kp = PIDcfg.Kp
        self.Ki = PIDcfg.Ki
        self.Kd = PIDcfg.Kd
        self.integral_limit = PIDcfg.integral_limit
        self.integral_e += e * dt
        self.integral_e = np.clip(
            self.integral_e,
            -self.integral_limit,
            self.integral_limit,
        )
        tau = self.Kp * e + self.Ki * self.integral_e  + self.Kd * de
        tau = np.clip(
            tau,
            -PIDcfg.TAU_LIMIT,
            PIDcfg.TAU_LIMIT,
        )
        return {
            "tau": tau,
            "qd": qd,
            "dqd": dqd,
            "ddqd": ddqd,
            "e": e,
            "de": de,
        }