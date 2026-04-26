"""
TikTok A/B Testing Dashboard
Interactive Streamlit app for exploring experiment results.
Author: Kalpana Joyce Dovari
"""

import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from scipy.stats import ttest_ind, chi2_contingency, sem, t
from pathlib import Path

st.set_page_config(
    page_title="TikTok A/B Lab",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=DM+Sans:wght@300;400;600&display=swap');
html, body, [class*="css"] {
    background-color: #0a0a0a;
    color: #e0e0e0;
    font-family: 'DM Sans', sans-serif;
}
h1, h2, h3 { font-family: 'Space Mono', monospace; }
.sig-badge {
    display: inline-block;
    padding: 4px 14px;
    border-radius: 20px;
    font-size: 13px;
    font-weight: 700;
    font-family: 'Space Mono', monospace;
}
.sig   { background: #003322; color: #00c853; border: 1px solid #00c853; }
.nosig { background: #2a0000; color: #fe2c55; border: 1px solid #fe2c55; }
.ship  { background: #001a33; color: #25f4ee; border: 1px solid #25f4ee; }
.nship { background: #1a1a00; color: #ffd700; border: 1px solid #ffd700; }
div[data-testid="stMetricValue"] {
    font-family: 'Space Mono', monospace;
    font-size: 28px !important;
    color: #25f4ee !important;
}
</style>
""", unsafe_allow_html=True)

PINK  = '#fe2c55'
CYAN  = '#25f4ee'
BG    = '#0a0a0a'

PLT_STYLE = {
    'figure.facecolor': BG,
    'axes.facecolor':   '#111111',
    'axes.edgecolor':   '#222222',
    'text.color':       '#e0e0e0',
    'axes.labelcolor':  '#cccccc',
    'xtick.color':      '#888888',
    'ytick.color':      '#888888',
    'grid.color':       '#1e1e1e',
    'grid.linestyle':   '--',
    'font.family':      'monospace',
}
plt.rcParams.update(PLT_STYLE)

@st.cache_data
def load_data():
    data_path = Path(__file__).parent.parent / "data" / "tiktok_ab_experiment_data.csv"
    return pd.read_csv(data_path)

df = load_data()

def cohens_d(a, b):
    pooled = np.sqrt((a.std()**2 + b.std()**2) / 2)
    return (b.mean() - a.mean()) / pooled

def effect_label(d):
    d = abs(d)
    if d < 0.2:   return 'Negligible'
    elif d < 0.5: return 'Small'
    elif d < 0.8: return 'Medium'
    else:         return 'Large'

def ci95(group):
    n = len(group)
    m = group.mean()
    h = sem(group) * t.ppf(0.975, n - 1)
    return m - h, m + h

def sig_badges(significant):
    if significant:
        return '<span class="sig-badge sig">✅ SIGNIFICANT</span> &nbsp; <span class="sig-badge ship">🚀 SHIP IT</span>'
    else:
        return '<span class="sig-badge nosig">❌ NOT SIGNIFICANT</span> &nbsp; <span class="sig-badge nship">⛔ DO NOT SHIP</span>'

with st.sidebar:
    st.markdown("## 🎬 TikTok A/B Lab")
    st.caption("Simulated experiment suite · 50,000 users")
    st.divider()
    experiment = st.selectbox("Select Experiment", [
        "Exp 1 — Recommendation Algorithm",
        "Exp 2 — Thumbnail Format",
        "Exp 3 — Notification Timing",
        "Exp 4 — Autoplay Toggle",
        "📊 Full Suite Summary",
    ])
    alpha = st.slider("Significance Threshold (α)", 0.01, 0.10, 0.05, 0.01, format="%.2f")
    st.divider()
    st.caption("Built by Kalpana Joyce Dovari")
    st.caption("[GitHub](https://github.com/kalpanajoycedovari) · [Portfolio](https://my-portfolio-taupe-kappa-13.vercel.app/)")

st.markdown("# 🎬 TikTok A/B Testing Dashboard")
st.markdown("*Simulating a real-world experimentation suite across 4 concurrent product tests*")
st.divider()

if experiment == "Exp 1 — Recommendation Algorithm":
    ctrl = df[df['exp1_group'] == 'control']['watch_time_seconds']
    trt  = df[df['exp1_group'] == 'treatment']['watch_time_seconds']
    t_stat, p_val = ttest_ind(ctrl, trt, equal_var=False)
    d = cohens_d(ctrl, trt)
    significant = p_val < alpha
    ci_c = ci95(ctrl)
    ci_t = ci95(trt)

    st.subheader("Exp 1 — New Recommendation Algorithm")
    st.markdown("**Hypothesis:** The updated recommendation model increases average watch time per video.")
    st.markdown("**Test:** Welch's T-Test &nbsp;|&nbsp; **Metric:** Watch Time (seconds)")
    st.divider()

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Control Mean",   f"{ctrl.mean():.1f}s", f"n={len(ctrl):,}")
    c2.metric("Treatment Mean", f"{trt.mean():.1f}s",  f"n={len(trt):,}")
    c3.metric("Lift", f"+{trt.mean()-ctrl.mean():.1f}s", f"{(trt.mean()-ctrl.mean())/ctrl.mean()*100:.1f}% relative")
    c4.metric("p-value", f"{p_val:.5f}", f"α = {alpha}")
    st.markdown(sig_badges(significant), unsafe_allow_html=True)
    st.caption(f"Cohen's d = {d:.4f} ({effect_label(d)} effect size) · t-statistic = {t_stat:.4f}")
    st.divider()

    col1, col2 = st.columns(2)
    with col1:
        fig, ax = plt.subplots(figsize=(7, 4))
        ax.hist(ctrl, bins=60, alpha=0.55, color=CYAN, label='Control',   density=True)
        ax.hist(trt,  bins=60, alpha=0.55, color=PINK, label='Treatment', density=True)
        ax.axvline(ctrl.mean(), color=CYAN, linestyle='--', lw=2)
        ax.axvline(trt.mean(),  color=PINK, linestyle='--', lw=2)
        ax.set_title('Watch Time Distribution', color='white')
        ax.set_xlabel('Watch Time (seconds)')
        ax.set_ylabel('Density')
        ax.legend(facecolor='#111', labelcolor='white', fontsize=9)
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        st.pyplot(fig)

    with col2:
        fig, ax = plt.subplots(figsize=(7, 4))
        means = [ctrl.mean(), trt.mean()]
        errs  = [ctrl.mean()-ci_c[0], trt.mean()-ci_t[0]]
        bars  = ax.bar(['Control', 'Treatment'], means, color=[CYAN, PINK], alpha=0.8, width=0.4)
        ax.errorbar(['Control', 'Treatment'], means, yerr=errs, fmt='none', color='white', capsize=10, lw=2)
        for bar, m in zip(bars, means):
            ax.text(bar.get_x()+bar.get_width()/2, m+1, f'{m:.1f}s', ha='center', color='white', fontweight='bold')
        ax.set_title('Mean Watch Time ± 95% CI', color='white')
        ax.set_ylabel('Watch Time (seconds)')
        ax.grid(True, alpha=0.3, axis='y')
        plt.tight_layout()
        st.pyplot(fig)

    with st.expander("📖 Why Welch's T-Test?"):
        st.markdown("""
        - T-tests compare the **means** of two groups to check if the difference is statistically significant.
        - **Welch's variant** does not assume equal variance between groups — safer for real A/B tests.
        - The **p-value** answers: if there were truly no difference, how likely is this result by chance?
        - If `p < α`, we reject the null hypothesis and conclude the treatment had a real impact.
        - **Cohen's d** measures practical significance — a tiny p-value with a negligible effect may not be worth shipping.
        """)

elif experiment == "Exp 2 — Thumbnail Format":
    ctrl = df[df['exp2_group'] == 'control']['clicked']
    trt  = df[df['exp2_group'] == 'treatment']['clicked']
    ct   = pd.crosstab(df['exp2_group'], df['clicked'])
    chi2, p_val, dof, _ = chi2_contingency(ct)
    significant = p_val < alpha
    ctrl_ctr  = ctrl.mean() * 100
    treat_ctr = trt.mean() * 100
    lift      = treat_ctr - ctrl_ctr

    st.subheader("Exp 2 — New Thumbnail Format")
    st.markdown("**Hypothesis:** Larger thumbnails increase click-through rate (CTR).")
    st.markdown("**Test:** Chi-Square Test &nbsp;|&nbsp; **Metric:** Clicked (binary 0/1)")
    st.divider()

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Control CTR",   f"{ctrl_ctr:.2f}%",  f"n={len(ctrl):,}")
    c2.metric("Treatment CTR", f"{treat_ctr:.2f}%", f"n={len(trt):,}")
    c3.metric("Lift", f"+{lift:.2f}pp", f"{lift/ctrl_ctr*100:.1f}% relative")
    c4.metric("p-value", f"{p_val:.6f}", f"χ² = {chi2:.2f}")
    st.markdown(sig_badges(significant), unsafe_allow_html=True)
    st.divider()

    col1, col2 = st.columns(2)
    with col1:
        fig, ax = plt.subplots(figsize=(7, 4))
        bars = ax.bar(['Control', 'Treatment'], [ctrl_ctr, treat_ctr], color=[CYAN, PINK], alpha=0.85, width=0.4)
        for bar, v in zip(bars, [ctrl_ctr, treat_ctr]):
            ax.text(bar.get_x()+bar.get_width()/2, v+0.05, f'{v:.2f}%', ha='center', color='white', fontweight='bold')
        ax.set_title('CTR by Group', color='white')
        ax.set_ylabel('Click-Through Rate (%)')
        ax.grid(True, alpha=0.3, axis='y')
        plt.tight_layout()
        st.pyplot(fig)

    with col2:
        fig, ax = plt.subplots(figsize=(7, 4))
        props = ct.div(ct.sum(axis=1), axis=0) * 100
        props.plot(kind='bar', stacked=True, ax=ax, color=['#1a1a1a', PINK], edgecolor='#333', rot=0, width=0.4)
        ax.set_title('Click Proportion by Group', color='white')
        ax.set_ylabel('Percentage (%)')
        ax.legend(['Not Clicked', 'Clicked'], facecolor='#111', labelcolor='white')
        ax.grid(True, alpha=0.3, axis='y')
        plt.tight_layout()
        st.pyplot(fig)

    with st.expander("📖 Why Chi-Square Test?"):
        st.markdown("""
        - CTR is a **binary outcome** — clicked or not. That makes it categorical, not continuous.
        - Chi-Square tests whether the **distribution of a categorical variable differs** between groups.
        - We build a **contingency table**: rows = experiment group, columns = clicked/not clicked.
        - If proportions are the same in both groups, χ² is small. If different enough, p < α.
        - A T-Test would be inappropriate here — Chi-Square is the correct choice for binary data.
        """)

elif experiment == "Exp 3 — Notification Timing":
    ctrl = df[df['exp3_group'] == 'control']['app_opens']
    trt  = df[df['exp3_group'] == 'treatment']['app_opens']
    t_stat, p_val = ttest_ind(ctrl, trt, equal_var=False)
    d = cohens_d(ctrl, trt)
    significant = p_val < alpha

    st.subheader("Exp 3 — Notification Timing")
    st.markdown("**Hypothesis:** Changing push notification timing increases daily app opens.")
    st.markdown("**Test:** Welch's T-Test &nbsp;|&nbsp; **Metric:** Daily App Opens")
    st.divider()

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Control Mean",   f"{ctrl.mean():.3f}", f"n={len(ctrl):,}")
    c2.metric("Treatment Mean", f"{trt.mean():.3f}",  f"n={len(trt):,}")
    c3.metric("Difference", f"{trt.mean()-ctrl.mean():.4f}", "Near zero")
    c4.metric("p-value", f"{p_val:.4f}", f"α = {alpha}")
    st.markdown(sig_badges(significant), unsafe_allow_html=True)
    st.caption(f"Cohen's d = {d:.4f} ({effect_label(d)} effect) — groups are virtually identical")
    st.divider()

    fig, ax = plt.subplots(figsize=(13, 4))
    ax.hist(ctrl, bins=60, alpha=0.55, color=CYAN, label='Control',   density=True)
    ax.hist(trt,  bins=60, alpha=0.55, color=PINK, label='Treatment', density=True)
    ax.axvline(ctrl.mean(), color=CYAN, linestyle='--', lw=2)
    ax.axvline(trt.mean(),  color=PINK, linestyle='--', lw=2)
    ax.set_title('App Opens Distribution — Groups Overlap Almost Perfectly', color='white')
    ax.set_xlabel('Daily App Opens')
    ax.set_ylabel('Density')
    ax.legend(facecolor='#111', labelcolor='white')
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    st.pyplot(fig)
    st.info("ℹ️ This experiment was designed with no real effect. The near-identical distributions and high p-value correctly lead us to conclude: do not ship.")

elif experiment == "Exp 4 — Autoplay Toggle":
    ctrl = df[df['exp4_group'] == 'control']['session_length_minutes']
    trt  = df[df['exp4_group'] == 'treatment']['session_length_minutes']
    t_stat, p_val = ttest_ind(ctrl, trt, equal_var=False)
    d = cohens_d(ctrl, trt)
    significant = p_val < alpha

    st.subheader("Exp 4 — Autoplay Toggle")
    st.markdown("**Hypothesis:** Enabling autoplay by default increases session length.")
    st.markdown("**Test:** Welch's T-Test &nbsp;|&nbsp; **Metric:** Session Length (minutes)")
    st.divider()

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Control Mean",   f"{ctrl.mean():.3f} min", f"n={len(ctrl):,}")
    c2.metric("Treatment Mean", f"{trt.mean():.3f} min",  f"n={len(trt):,}")
    c3.metric("Difference", f"{trt.mean()-ctrl.mean():.4f} min", "Near zero")
    c4.metric("p-value", f"{p_val:.4f}", f"α = {alpha}")
    st.markdown(sig_badges(significant), unsafe_allow_html=True)
    st.caption(f"Cohen's d = {d:.4f} ({effect_label(d)} effect)")
    st.divider()

    fig, ax = plt.subplots(figsize=(13, 4))
    ax.hist(ctrl, bins=60, alpha=0.55, color=CYAN, label='Control',   density=True)
    ax.hist(trt,  bins=60, alpha=0.55, color=PINK, label='Treatment', density=True)
    ax.axvline(ctrl.mean(), color=CYAN, linestyle='--', lw=2)
    ax.axvline(trt.mean(),  color=PINK, linestyle='--', lw=2)
    ax.set_title('Session Length Distribution — No Signal Detected', color='white')
    ax.set_xlabel('Session Length (minutes)')
    ax.set_ylabel('Density')
    ax.legend(facecolor='#111', labelcolor='white')
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    st.pyplot(fig)
    st.info("ℹ️ Autoplay had no statistically significant effect on session length. Do not ship.")

else:
    st.subheader("📊 Full Experiment Suite — Executive Summary")
    st.markdown("*4 concurrent experiments · 50,000 users · Q2 2026 simulation*")
    st.divider()

    e1_ctrl = df[df['exp1_group']=='control']['watch_time_seconds']
    e1_trt  = df[df['exp1_group']=='treatment']['watch_time_seconds']
    _, p1   = ttest_ind(e1_ctrl, e1_trt, equal_var=False)

    e2_ctrl = df[df['exp2_group']=='control']['clicked']
    e2_trt  = df[df['exp2_group']=='treatment']['clicked']
    ct      = pd.crosstab(df['exp2_group'], df['clicked'])
    _, p2, _, _ = chi2_contingency(ct)

    e3_ctrl = df[df['exp3_group']=='control']['app_opens']
    e3_trt  = df[df['exp3_group']=='treatment']['app_opens']
    _, p3   = ttest_ind(e3_ctrl, e3_trt, equal_var=False)

    e4_ctrl = df[df['exp4_group']=='control']['session_length_minutes']
    e4_trt  = df[df['exp4_group']=='treatment']['session_length_minutes']
    _, p4   = ttest_ind(e4_ctrl, e4_trt, equal_var=False)

    rows = [
        {"Experiment": "Exp 1: Recommendation Algorithm", "Metric": "Watch Time (s)",      "Test": "Welch T-Test", "Control": round(e1_ctrl.mean(),2), "Treatment": round(e1_trt.mean(),2), "p-value": round(p1,5), "Decision": "🚀 SHIP" if p1 < alpha else "⛔ HOLD"},
        {"Experiment": "Exp 2: Thumbnail Format",         "Metric": "CTR (%)",              "Test": "Chi-Square",   "Control": round(e2_ctrl.mean()*100,2), "Treatment": round(e2_trt.mean()*100,2), "p-value": round(p2,6), "Decision": "🚀 SHIP" if p2 < alpha else "⛔ HOLD"},
        {"Experiment": "Exp 3: Notification Timing",      "Metric": "App Opens",            "Test": "Welch T-Test", "Control": round(e3_ctrl.mean(),3), "Treatment": round(e3_trt.mean(),3), "p-value": round(p3,4), "Decision": "🚀 SHIP" if p3 < alpha else "⛔ HOLD"},
        {"Experiment": "Exp 4: Autoplay Toggle",          "Metric": "Session Length (min)", "Test": "Welch T-Test", "Control": round(e4_ctrl.mean(),3), "Treatment": round(e4_trt.mean(),3), "p-value": round(p4,4), "Decision": "🚀 SHIP" if p4 < alpha else "⛔ HOLD"},
    ]

    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
    st.divider()
    st.markdown(f"""
    ### Key Insight
    **2 of 4 experiments showed statistically significant effects** at α = {alpha:.2f}.
    This mirrors reality — most product changes do not move the metric they target.

    | Finding | Why it matters |
    |---|---|
    | Exp 1 & 2 significant | Real measurable impact on user behaviour |
    | Exp 3 & 4 not significant | No detectable effect — do not ship |
    | Cohen's d computed | Practical significance, not just statistical |
    | Welch's T-Test | Doesn't assume equal variance between groups |
    | Chi-Square for CTR | Correct test for binary outcomes |
    """)
    st.caption("Adjust α in the sidebar to see how the threshold affects decisions.")