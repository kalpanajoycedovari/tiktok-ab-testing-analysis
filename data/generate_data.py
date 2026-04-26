"""
TikTok A/B Testing Synthetic Data Generator
============================================
Generates realistic user experiment data simulating TikTok's
internal experimentation platform across 4 concurrent experiments.

Distributions calibrated against publicly reported industry benchmarks:
- Average TikTok session: ~10 minutes
- Video completion rate: ~50-60%
- Average CTR on feed: ~3-6%
- Daily app opens: ~8-10 per active user

Author: Kalpana Joyce Dovari
"""

import numpy as np
import pandas as pd
from pathlib import Path

np.random.seed(42)
N_USERS = 50_000

# ── User base ──────────────────────────────────────────────────────────────
def generate_users(n: int) -> pd.DataFrame:
    ages = np.random.normal(loc=24, scale=6, size=n).clip(13, 60).astype(int)
    countries = np.random.choice(
        ["US", "UK", "IN", "BR", "ID", "MX", "DE", "FR"],
        size=n,
        p=[0.25, 0.10, 0.20, 0.10, 0.10, 0.08, 0.09, 0.08],
    )
    device = np.random.choice(["iOS", "Android"], size=n, p=[0.45, 0.55])
    tenure_days = np.random.exponential(scale=180, size=n).clip(1, 730).astype(int)

    return pd.DataFrame({
        "user_id": [f"u_{i:06d}" for i in range(n)],
        "age": ages,
        "country": countries,
        "device": device,
        "tenure_days": tenure_days,
    })


# ── Experiment 1: Recommendation Algorithm → Watch Time (seconds) ──────────
# Treatment has a REAL effect (+12s avg). T-test should be significant.
def add_experiment_1(df: pd.DataFrame) -> pd.DataFrame:
    group = np.random.choice(["control", "treatment"], size=len(df))
    base_watch = np.random.normal(loc=180, scale=55, size=len(df)).clip(5, 600)
    effect = np.where(group == "treatment",
                      np.random.normal(loc=12, scale=5, size=len(df)), 0)
    watch_time = (base_watch + effect).clip(5, 600).round(1)

    df["exp1_group"] = group
    df["watch_time_seconds"] = watch_time
    return df


# ── Experiment 2: Thumbnail Format → Clicked (0/1) ────────────────────────
# Treatment has a REAL effect (CTR 4% → 5.8%). Chi-square should be significant.
def add_experiment_2(df: pd.DataFrame) -> pd.DataFrame:
    group = np.random.choice(["control", "treatment"], size=len(df))
    ctr = np.where(group == "control", 0.04, 0.058)
    clicked = np.random.binomial(n=1, p=ctr, size=len(df))

    df["exp2_group"] = group
    df["clicked"] = clicked
    return df


# ── Experiment 3: Notification Timing → App Opens ─────────────────────────
# NO real effect — both groups similar. Should NOT be significant.
def add_experiment_3(df: pd.DataFrame) -> pd.DataFrame:
    group = np.random.choice(["control", "treatment"], size=len(df))
    base_opens = np.random.normal(loc=8.5, scale=3.2, size=len(df)).clip(0, 30)
    # tiny noise — no real signal
    noise = np.random.normal(loc=0.1, scale=0.3, size=len(df))
    app_opens = (base_opens + noise).clip(0, 30).round(1)

    df["exp3_group"] = group
    df["app_opens"] = app_opens
    return df


# ── Experiment 4: Autoplay Toggle → Session Length (minutes) ──────────────
# NO real effect. Should NOT be significant.
def add_experiment_4(df: pd.DataFrame) -> pd.DataFrame:
    group = np.random.choice(["control", "treatment"], size=len(df))
    base_session = np.random.normal(loc=10.2, scale=4.8, size=len(df)).clip(0.5, 45)
    noise = np.random.normal(loc=0.05, scale=0.5, size=len(df))
    session_length = (base_session + noise).clip(0.5, 45).round(2)

    df["exp4_group"] = group
    df["session_length_minutes"] = session_length
    return df


# ── Build and save ─────────────────────────────────────────────────────────
def generate(output_dir: str = ".") -> pd.DataFrame:
    print(f"Generating {N_USERS:,} synthetic users...")
    df = generate_users(N_USERS)
    df = add_experiment_1(df)
    df = add_experiment_2(df)
    df = add_experiment_3(df)
    df = add_experiment_4(df)

    out = Path(output_dir) / "tiktok_ab_experiment_data.csv"
    df.to_csv(out, index=False)
    print(f"Saved → {out}  ({df.shape[0]:,} rows × {df.shape[1]} cols)")
    return df


if __name__ == "__main__":
    generate(output_dir=Path(__file__).parent)
