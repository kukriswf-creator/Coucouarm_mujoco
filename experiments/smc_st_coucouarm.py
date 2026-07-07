import time
import numpy as np
import mujoco
import mujoco.viewer 

from coucouarm.config import SMC_ST_config as cfg
from coucouarm.trajectory.sine_reference_continuous import SineReference
from coucouarm.controllers.smc_with_super_twisting_controller import SMC_ST_Controller
from coucouarm.utils.csv_logger import CsvLogger 


def build_header(): 
    return (
        ["time"]
        + [f"q_des_{i+1}" for i in range(cfg.N_JOINT)]
        + [f"q_{i+1}" for i in range(cfg.N_JOINT)]
        + [f"err_{i+1}" for i in range(cfg.N_JOINT)]
        + [f"dq_{i+1}" for i in range(cfg.N_JOINT)]
        + [f"tau_{i+1}" for i in range(cfg.N_JOINT)]
        + [f"s_{i+1}" for i in range(cfg.N_JOINT)]
    )


def main():
    model = mujoco.MjModel.from_xml_path(cfg.URDF_PATH)
    data = mujoco.MjData(model)
   
    model.opt.timestep = cfg.DT
   
    model.opt.disableflags |= mujoco.mjtDisableBit.mjDSBL_CONTACT
   
    model.dof_damping[:] = np.zeros(model.nv)
  
    data.qpos[:] = cfg.Q_INIT 
    data.qvel[:] = 0.0 
    data.qfrc_applied[:] = 0.0 
    data.xfrc_applied[:, :] = 0.0 
    mujoco.mj_forward(model, data) 

    reference = SineReference() 
    controller = SMC_ST_Controller(model, data, reference) 

    logger = CsvLogger(cfg.LOG_PATH, build_header())

    print("MuJoCo model ok.")

    try:
        with mujoco.viewer.launch_passive(model, data) as viewer:
            step_count = 0

            while viewer.is_running(): 
                t = data.time
                dt = model.opt.timestep
                q = data.qpos.copy()
                dq = data.qvel.copy()

                result = controller.compute(t, q, dq, dt)

                tau_raw = result["tau"]
                qd = result["qd"]
                e = result["e"]
                s = result["s"]

                tau = np.clip(tau_raw, -cfg.TAU_LIMIT, cfg.TAU_LIMIT)
                
                data.qfrc_applied[:] = tau 
                mujoco.mj_step(model, data) 

                logger.append([
                    t,
                    *qd,
                    *q,
                    *e,
                    *dq,
                    *tau,
                    *s,
                ])

                if step_count % cfg.RENDER_EVERY == 0:
                    viewer.sync()

                if step_count % 250 == 0: 
                    print("time:", round(t, 3))
                    print("e:", np.round(e, 3))
                    print("s:", np.round(s, 3))
                    print("tau:", np.round(tau, 3))
                    print("Oo" * 20)
                step_count += 1 

    except KeyboardInterrupt:
        print("\nSimulation stopped by Ctrl+C.")

    finally:
        logger.save() 


if __name__ == "__main__":
    main()