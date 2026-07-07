import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


CSV_PATH = "/home/liu/coucouarm_v5/mujoco/data/csv/smc_st_log.csv"
FIG_DIR = "/home/liu/coucouarm_v5/mujoco/data/figures"

N_JOINT = 6


def get_series(df, name):
    if name not in df.columns:
        raise KeyError(f"CSV 中找不到列: {name}")
    return df[name].to_numpy()


def rmse(x):
    x = np.asarray(x)
    return float(np.sqrt(np.mean(x ** 2)))


def save_fig(fig, filename):
    os.makedirs(FIG_DIR, exist_ok=True)

    path = os.path.join(FIG_DIR, filename)
    fig.tight_layout()
    fig.savefig(path, dpi=200)
    plt.close(fig)

    print("Saved:", path)


def plot_q_tracking(df):
    t = get_series(df, "time")

    fig, axes = plt.subplots(N_JOINT, 1, figsize=(14, 12), sharex=True)

    for i in range(1, N_JOINT + 1):
        ax = axes[i - 1]

        q_des = get_series(df, f"q_des_{i}")
        q = get_series(df, f"q_{i}")

        ax.plot(t, q_des, label=f"joint_{i} q_des")
        ax.plot(t, q, linestyle="--", label=f"joint_{i} q")

        ax.set_ylabel("rad")
        ax.grid(True)
        ax.legend(loc="upper right")

    axes[-1].set_xlabel("time / s")
    fig.suptitle("PTSMC Trajectory Tracking: q_des vs q")

    save_fig(fig, "01_q_des_vs_q.png")


def plot_error(df):

    t = get_series(df, "time")

    fig, axes = plt.subplots(N_JOINT, 1, figsize=(14, 12), sharex=True)

    for i in range(1, N_JOINT + 1):
        ax = axes[i - 1]

        err_rad = get_series(df, f"err_{i}")
        err_deg = np.rad2deg(err_rad)

        ax.plot(t, err_deg, label=f"joint_{i} error")

        ax.set_ylabel("deg")
        ax.grid(True)
        ax.legend(loc="upper right")

    axes[-1].set_xlabel("time / s")
    fig.suptitle("PTSMC Tracking Error")

    save_fig(fig, "02_tracking_error_deg.png")


def plot_tau(df):
   
    t = get_series(df, "time")

    fig, axes = plt.subplots(N_JOINT, 1, figsize=(14, 12), sharex=True)

    for i in range(1, N_JOINT + 1):
        ax = axes[i - 1]
        tau = get_series(df, f"tau_{i}")
        ax.plot(t, tau, label=f"joint_{i} tau")
        ax.set_ylabel("N·m")
        ax.grid(True)
        ax.legend(loc="upper right")

    axes[-1].set_xlabel("time / s")
    fig.suptitle("PTSMC Control Torque")

    save_fig(fig, "03_control_torque.png")


def plot_dq(df):
   
    t = get_series(df, "time")

    fig, axes = plt.subplots(N_JOINT, 1, figsize=(14, 12), sharex=True)

    for i in range(1, N_JOINT + 1):
        ax = axes[i - 1]

        dq = get_series(df, f"dq_{i}")

        ax.plot(t, dq, label=f"joint_{i} dq")

        ax.set_ylabel("rad/s")
        ax.grid(True)
        ax.legend(loc="upper right")

    axes[-1].set_xlabel("time / s")
    fig.suptitle("Joint Velocity dq")

    save_fig(fig, "04_joint_velocity.png")


def plot_s(df):
   
    t = get_series(df, "time")

    fig, axes = plt.subplots(N_JOINT, 1, figsize=(14, 12), sharex=True)

    for i in range(1, N_JOINT + 1):
        ax = axes[i - 1]

        s = get_series(df, f"s_{i}")

        ax.plot(t, s, label=f"joint_{i} s")

        ax.set_ylabel("sliding surface")
        ax.grid(True)
        ax.legend(loc="upper right")

    axes[-1].set_xlabel("time / s")
    fig.suptitle("Joint Sliding Surface")

    save_fig(fig, "05_sliding surface.png")

def write_metrics(df):
   
    os.makedirs(FIG_DIR, exist_ok=True)

    metrics_path = os.path.join(FIG_DIR, "metrics_summary.txt")

    lines = []
    lines.append("PTSMC trajectory tracking metrics")
    lines.append("=" * 60)
    lines.append(f"CSV_PATH: {CSV_PATH}")
    lines.append("")

    t = get_series(df, "time")
    lines.append(f"time_start: {t[0]:.4f} s")
    lines.append(f"time_end:   {t[-1]:.4f} s")
    lines.append(f"sample_num: {len(t)}")
    lines.append("")

    for i in range(1, N_JOINT + 1):
        err_rad = get_series(df, f"err_{i}")
        err_deg = np.rad2deg(err_rad)

        tau = get_series(df, f"tau_{i}")
        dq = get_series(df, f"dq_{i}")

        q_des = get_series(df, f"q_des_{i}")
        q = get_series(df, f"q_{i}")

        lines.append(f"joint_{i}")
        lines.append("-" * 60)
        lines.append(f"max_abs_error: {np.max(np.abs(err_deg)):.6f} deg")
        lines.append(f"rmse_error:    {rmse(err_deg):.6f} deg")
        lines.append(f"mean_error:    {np.mean(err_deg):.6f} deg")
        lines.append(f"max_abs_tau:   {np.max(np.abs(tau)):.6f} N·m")
        lines.append(f"rmse_tau:      {rmse(tau):.6f} N·m")
        lines.append(f"max_abs_dq:    {np.max(np.abs(dq)):.6f} rad/s")
        lines.append(f"q_des_range:   [{np.min(q_des):.6f}, {np.max(q_des):.6f}] rad")
        lines.append(f"q_range:       [{np.min(q):.6f}, {np.max(q):.6f}] rad")
        lines.append("")

    with open(metrics_path, "w") as f:
        f.write("\n".join(lines))

    print("Saved:", metrics_path)
    print("\n".join(lines))


def main():
    if not os.path.exists(CSV_PATH):
        raise FileNotFoundError(
            f"找不到 CSV 文件: {CSV_PATH}\n"

        )

    os.makedirs(FIG_DIR, exist_ok=True)

    df = pd.read_csv(CSV_PATH)

    required_columns = (
        ["time"] +
        [f"q_des_{i+1}" for i in range(N_JOINT)] +
        [f"q_{i+1}" for i in range(N_JOINT)] +
        [f"err_{i+1}" for i in range(N_JOINT)] +
        [f"dq_{i+1}" for i in range(N_JOINT)] +
        [f"tau_{i+1}" for i in range(N_JOINT)]+
        [f"s_{i+1}" for i in range(N_JOINT)]
    )

    for col in required_columns:
        if col not in df.columns:
            raise KeyError(f"CSV 缺少必要列: {col}")

    print("CSV loaded:", CSV_PATH)
    print("rows:", len(df))
    print("columns:", len(df.columns))
    print("figures dir:", FIG_DIR)

    plot_q_tracking(df)
    plot_error(df)
    plot_tau(df)
    plot_dq(df)
    plot_s(df)
    write_metrics(df)

    print("\nAll figures saved to:", FIG_DIR)


if __name__ == "__main__":
    main()
