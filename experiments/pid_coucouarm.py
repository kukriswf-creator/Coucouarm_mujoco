import time
import numpy as np
import mujoco
import mujoco.viewer 

from coucouarm.config import PID_config as PIDcfg
from coucouarm.trajectory.sine_reference_continuous import SineReference
from coucouarm.controllers.pid_controller import PIDController
from coucouarm.utils.csv_logger import CsvLogger 


def build_header():
    return (
        ["time"]
        + [f"q_des_{i+1}" for i in range(PIDcfg.N_JOINT)]
        + [f"q_{i+1}" for i in range(PIDcfg.N_JOINT)]
        + [f"err_{i+1}" for i in range(PIDcfg.N_JOINT)]
        + [f"dq_{i+1}" for i in range(PIDcfg.N_JOINT)]
        + [f"tau_{i+1}" for i in range(PIDcfg.N_JOINT)]
    )


def main():
    model = mujoco.MjModel.from_xml_path(PIDcfg.URDF_PATH)
    data = mujoco.MjData(model)
    model.opt.disableflags |= mujoco.mjtDisableBit.mjDSBL_CONTACT
    data.qpos[:] = PIDcfg.Q_INIT 
    data.qvel[:] = 0.0 
    mujoco.mj_forward(model, data) 

    reference = SineReference() 
    controller = PIDController(reference) 
    
    logger = CsvLogger(PIDcfg.LOG_PATH, build_header())

    print("MuJoCo model ok.")

    try:
        with mujoco.viewer.launch_passive(model, data) as viewer:
            step_count = 0

            while viewer.is_running(): 
                t = data.time
                q = data.qpos.copy()
                dq = data.qvel.copy()
                dt = PIDcfg.DT
                result = controller.tau_pid(t, q, dq, dt)

                tau = result["tau"]
                qd = result["qd"]
                e = result["e"]

                data.qfrc_applied[:] = tau 
                mujoco.mj_step(model, data) 
                logger.append([ t,*qd, *q,*e,*dq,*tau,])

                if step_count % PIDcfg.RENDER_EVERY == 0:
                    viewer.sync()

                if step_count % 250 == 0: 
                    print("time:", round(t, 3))
                    print("e:", np.round(e, 3))
                    print("tau:", np.round(tau, 3))
                    print("-" * 50)
                step_count += 1 

    except KeyboardInterrupt:
        print("\nSimulation stopped by Ctrl+C.")

    finally:
        logger.save() 


if __name__ == "__main__":
    main()