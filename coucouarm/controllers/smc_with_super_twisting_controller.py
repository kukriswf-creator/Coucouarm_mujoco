import numpy as np
from coucouarm.config import SMC_ST_config as cfg
from coucouarm.dynamics.mujoco_dynamics import get_mujoco_dynamics


class SMC_ST_Controller:
    def __init__(self, model_ctrl, data_ctrl, reference):
        self.model_ctrl = model_ctrl
        self.data_ctrl = data_ctrl
        self.reference = reference
        self.nu = np.zeros(6)

    def st_reach_term(self,s,dt):
        nu_dot = -cfg.k2 * np.sign(s)
        self.nu += nu_dot * dt
        sigma = np.clip(s / cfg.phi, -1.0, 1.0)
        tau_sw = -cfg.k1 * np.sqrt(np.abs(s) + 1e-8) * sigma + self.nu

        return tau_sw
    
    def compute(self, t, q, dq, dt):
        M_ctrl, bias_ctrl = get_mujoco_dynamics(
            self.model_ctrl,
            self.data_ctrl,
            q,
            dq,
        )

        qd, dqd, ddqd = self.reference.get(t)
        e = qd - q
        de = dqd - dq

        s = de + cfg.alpha * e

        tau_sw = self.st_reach_term(s,dt)

        v = ddqd + cfg.alpha * de - tau_sw

        tau = M_ctrl @ v + bias_ctrl

        return {
            "tau": tau,
            "qd": qd,
            "dqd": dqd,
            "ddqd": ddqd,
            "e": e,
            "de": de,
            "s": s,
            "v": v,
            "M_ctrl": M_ctrl,
            "bias_ctrl": bias_ctrl,
        }