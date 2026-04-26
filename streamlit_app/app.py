"""
TikTok A/B Testing Dashboard — Stakeholder Edition
A clean, executive-facing experimentation report.
Author: Kalpana Joyce Dovari
"""

import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from scipy.stats import ttest_ind, chi2_contingency, sem, t
from pathlib import Path

st.set_page_config(
    page_title="TikTok Experiment Review — Q2 2026",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=IBM+Plex+Sans:wght@300;400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap');
html, body, [class*="css"] {
    background-color: #F7F6F2;
    color: #1a1a1a;
    font-family: 'IBM Plex Sans', sans-serif;
}
h1, h2, h3 { font-family: 'Playfair Display', serif; color: #111; }
.header-band {
    background: #111; color: #F7F6F2;
    padding: 40px 48px 32px; margin: -1rem -1rem 2rem -1rem;
    border-bottom: 3px solid #E8C547;
}
.header-band h1 { font-family: 'Playfair Display', serif; font-size: 2rem; color: #F7F6F2; margin: 0 0 6px 0; }
.header-band p  { font-family: 'IBM Plex Sans', sans-serif; font-size: 0.85rem; color: #999; margin: 0; letter-spacing: 0.08em; text-transform: uppercase; }
.verdict-card { background: white; border-radius: 4px; padding: 24px; border-left: 4px solid #ccc; box-shadow: 0 1px 4px rgba(0,0,0,0.06); margin-bottom: 12px; }
.verdict-card.ship { border-left-color: #2A7F5F; }
.verdict-card.hold { border-left-color: #C0392B; }
.verdict-label { font-family: 'IBM Plex Mono', monospace; font-size: 0.7rem; font-weight: 600; letter-spacing: 0.12em; text-transform: uppercase; padding: 3px 10px; border-radius: 2px; display: inline-block; margin-bottom: 10px; }
.label-ship { background: #E8F5EF; color: #2A7F5F; }
.label-hold { background: #FDEDEC; color: #C0392B; }
.exp-name { font-family: 'Playfair Display', serif; font-size: 1.05rem; font-weight: 600; color: #111; margin: 0 0 4px 0; }
.exp-metric { font-size: 0.82rem; color: #666; }
.big-lift { font-family: 'IBM Plex Mono', monospace; font-size: 1.4rem; font-weight: 600; margin-top: 12px; }
.lift-green { color: #2A7F5F; }
.lift-grey  { color: #aaa; }
.section-label { font-family: 'IBM Plex Mono', monospace; font-size: 0.7rem; letter-spacing: 0.15em; text-transform: uppercase; color: #999; margin-bottom: 16px; border-bottom: 1px solid #E5E5E5; padding-bottom: 8px; }
.story-block { background: white; border-radius: 4px; padding: 32px 36px; box-shadow: 0 1px 4px rgba(0,0,0,0.06); margin-bottom: 20px; }
.recommendation-box { padding: 20px 24px; border-radius: 4px; margin-top: 24px; }
.rec-ship { background: #E8F5EF; border-left: 3px solid #2A7F5F; }
.rec-hold { background: #FDEDEC; border-left: 3px solid #C0392B; }
.rec-title { font-family: 'IBM Plex Mono', monospace; font-size: 0.75rem; letter-spacing: 0.1em; text-transform: uppercase; font-weight: 600; margin-bottom: 6px; }
.rec-ship .rec-title { color: #2A7F5F; }
.rec-hold .rec-title { color: #C0392B; }
.rec-body { font-size: 0.9rem; color: #333; line-height: 1.6; }
.footnote { font-size: 0.75rem; color: #aaa; font-family: 'IBM Plex Mono', monospace; margin-top: 8px; }
div[data-testid="stMetricValue"] { font-family: 'IBM Plex Mono', monospace !important; color: #111 !important; }
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    data_path = Path(__file__).parent.parent / "data" / "tiktok_ab_experiment_data.csv"
    return pd.read_csv(data_path)

df = load_data()

def cohens_d(a, b):
    pooled = np.sqrt((a.std()**2 + b.std()**2) / 2)
    return (b.mean() - a.mean()) / pooled

def ci95(group):
    n, m = len(group), group.mean()
    h = sem(group) * t.ppf(0.975, n - 1)
    return m - h, m + h

def effect_label(d):
    d = abs(d)
    if d < 0.2: return 'negligible'
    elif d < 0.5: return 'small'
    elif d < 0.8: return 'medium'
    else: return 'large'

e1c = df[df['exp1_group']=='control']['watch_time_seconds']
e1t = df[df['exp1_group']=='treatment']['watch_time_seconds']
_, p1 = ttest_ind(e1c, e1t, equal_var=False)
d1   = cohens_d(e1c, e1t)

e2c = df[df['exp2_group']=='control']['clicked']
e2t = df[df['exp2_group']=='treatment']['clicked']
ct2 = pd.crosstab(df['exp2_group'], df['clicked'])
_, p2, _, _ = chi2_contingency(ct2)

e3c = df[df['exp3_group']=='control']['app_opens']
e3t = df[df['exp3_group']=='treatment']['app_opens']
_, p3 = ttest_ind(e3c, e3t, equal_var=False)
d3   = cohens_d(e3c, e3t)

e4c = df[df['exp4_group']=='control']['session_length_minutes']
e4t = df[df['exp4_group']=='treatment']['session_length_minutes']
_, p4 = ttest_ind(e4c, e4t, equal_var=False)
d4   = cohens_d(e4c, e4t)

ALPHA = 0.05

results = [
    {"id": 1, "name": "Recommendation Algorithm", "metric": "Avg. Watch Time",
     "ctrl": e1c.mean(), "trt": e1t.mean(), "unit": "s",
     "lift": e1t.mean()-e1c.mean(), "lift_pct": (e1t.mean()-e1c.mean())/e1c.mean()*100,
     "p": p1, "d": d1, "ship": p1 < ALPHA, "test": "Welch's T-Test",
     "what": "We tested a new recommendation algorithm that reranks the For You feed using updated engagement signals.",
     "result": f"Users shown the new algorithm watched an average of {e1t.mean():.1f}s per video, compared to {e1c.mean():.1f}s in the control group — a lift of +{e1t.mean()-e1c.mean():.1f}s (+{(e1t.mean()-e1c.mean())/e1c.mean()*100:.1f}%).",
     "rec": "The improvement is statistically significant and practically meaningful. We recommend shipping this algorithm to 100% of users in the next release cycle.",
     "ctrl_data": e1c, "trt_data": e1t},
    {"id": 2, "name": "Thumbnail Format", "metric": "Click-Through Rate",
     "ctrl": e2c.mean()*100, "trt": e2t.mean()*100, "unit": "%",
     "lift": (e2t.mean()-e2c.mean())*100, "lift_pct": (e2t.mean()-e2c.mean())/e2c.mean()*100,
     "p": p2, "d": None, "ship": p2 < ALPHA, "test": "Chi-Square Test",
     "what": "We tested a larger thumbnail format in the feed to determine whether it increases the likelihood of users clicking into a video.",
     "result": f"The new thumbnail format achieved a CTR of {e2t.mean()*100:.2f}%, up from {e2c.mean()*100:.2f}% in control — a lift of +{(e2t.mean()-e2c.mean())*100:.2f} percentage points.",
     "rec": "CTR improvement is statistically significant. The new thumbnail format should be rolled out across all feed surfaces. We recommend monitoring for any downstream effects on watch time.",
     "ctrl_data": e2c, "trt_data": e2t},
    {"id": 3, "name": "Notification Timing", "metric": "Daily App Opens",
     "ctrl": e3c.mean(), "trt": e3t.mean(), "unit": "",
     "lift": e3t.mean()-e3c.mean(), "lift_pct": (e3t.mean()-e3c.mean())/e3c.mean()*100,
     "p": p3, "d": d3, "ship": p3 < ALPHA, "test": "Welch's T-Test",
     "what": "We tested a new push notification send time, hypothesising that better timing would drive more daily app opens.",
     "result": f"Both groups averaged approximately {e3c.mean():.1f} daily app opens. The difference of {abs(e3t.mean()-e3c.mean()):.3f} opens is not statistically significant.",
     "rec": "There is no evidence that the new notification timing improves re-engagement. We recommend holding this change and testing alternative notification content instead.",
     "ctrl_data": e3c, "trt_data": e3t},
    {"id": 4, "name": "Autoplay Toggle", "metric": "Session Length",
     "ctrl": e4c.mean(), "trt": e4t.mean(), "unit": " min",
     "lift": e4t.mean()-e4c.mean(), "lift_pct": (e4t.mean()-e4c.mean())/e4c.mean()*100,
     "p": p4, "d": d4, "ship": p4 < ALPHA, "test": "Welch's T-Test",
     "what": "We tested enabling autoplay by default, expecting it to reduce friction between videos and extend session length.",
     "result": f"Session lengths were nearly identical: {e4c.mean():.2f} min (control) vs {e4t.mean():.2f} min (treatment). The difference is not statistically significant.",
     "rec": "Autoplay default did not extend sessions. Given potential negative user sentiment around autoplay, we recommend not shipping this change.",
     "ctrl_data": e4c, "trt_data": e4t},
]

PLT = {
    'figure.facecolor': 'white', 'axes.facecolor': 'white',
    'axes.edgecolor': '#E5E5E5', 'axes.spines.top': False, 'axes.spines.right': False,
    'text.color': '#333', 'axes.labelcolor': '#555',
    'xtick.color': '#888', 'ytick.color': '#888',
    'grid.color': '#F0F0F0', 'grid.linestyle': '-', 'font.family': 'sans-serif',
}
plt.rcParams.update(PLT)
GREEN = '#2A7F5F'; RED = '#C0392B'; GREY = '#CCCCCC'

st.markdown("""
<div class="header-band">
    <p>TikTok · Product Experimentation · Q2 2026</p>
    <h1>Experiment Review</h1>
    <p style="margin-top:8px; color:#666;">4 experiments · 50,000 users · Prepared by Kalpana Joyce Dovari</p>
</div>
""", unsafe_allow_html=True)

pages = ["Overview", "Exp 1 — Recommendation Algorithm", "Exp 2 — Thumbnail Format",
         "Exp 3 — Notification Timing", "Exp 4 — Autoplay Toggle"]
page = st.selectbox("", pages, label_visibility="collapsed")
st.markdown("<div style='margin-bottom:24px'></div>", unsafe_allow_html=True)

if page == "Overview":
    st.markdown("<div class='section-label'>Experiment Results at a Glance</div>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    for i, r in enumerate(results):
        col = col1 if i % 2 == 0 else col2
        card_class  = "ship" if r["ship"] else "hold"
        label_class = "label-ship" if r["ship"] else "label-hold"
        label_text  = "✓ Recommended to ship" if r["ship"] else "✗ Do not ship"
        lift_class  = "lift-green" if r["ship"] else "lift-grey"
        lift_str    = f"+{r['lift']:.1f}{r['unit']}" if r["ship"] else f"{r['lift']:+.3f}{r['unit']}"
        with col:
            st.markdown(f"""
            <div class="verdict-card {card_class}">
                <span class="verdict-label {label_class}">{label_text}</span>
                <div class="exp-name">Exp {r['id']}: {r['name']}</div>
                <div class="exp-metric">Measuring {r['metric']}</div>
                <div class="big-lift {lift_class}">{lift_str} lift</div>
                <div class="footnote">p = {r['p']:.5f} · {r['test']}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<div class='section-label'>Summary</div>", unsafe_allow_html=True)
    shipped = sum(1 for r in results if r["ship"])
    st.markdown(f"""
    <div class="story-block">
        <p style="font-size:1rem; line-height:1.8; color:#333;">
        Of the 4 experiments run this quarter, <strong>{shipped} produced statistically significant results</strong>
        and are recommended for release. The recommendation algorithm and thumbnail format changes
        both showed clear, measurable improvements to core engagement metrics.
        The notification timing and autoplay experiments did not produce significant effects
        and should not be shipped in their current form.
        </p>
        <p style="font-size:0.85rem; color:#888; margin-top:16px;">
        All results evaluated at α = 0.05. Select an experiment above for the full analysis.
        </p>
    </div>
    """, unsafe_allow_html=True)

    fig, ax = plt.subplots(figsize=(10, 3.5))
    names  = [f"Exp {r['id']}: {r['name']}" for r in results]
    lifts  = [r['lift_pct'] for r in results]
    colors = [GREEN if r['ship'] else '#DDDDDD' for r in results]
    bars   = ax.barh(names, lifts, color=colors, height=0.5)
    ax.axvline(0, color='#333', lw=0.8)
    for bar, val, r in zip(bars, lifts, results):
        xpos = val + 0.2 if val >= 0 else val - 0.2
        ha   = 'left' if val >= 0 else 'right'
        ax.text(xpos, bar.get_y()+bar.get_height()/2, f"{val:+.1f}%",
                va='center', ha=ha, fontsize=9,
                color=GREEN if r['ship'] else '#999',
                fontfamily='monospace', fontweight='600')
    ax.set_xlabel('Relative Lift (%)', fontsize=9)
    ax.set_title('Relative lift by experiment', fontsize=10, color='#444', pad=12)
    ax.grid(True, axis='x', alpha=0.4)
    patches = [mpatches.Patch(color=GREEN, label='Recommended to ship'),
               mpatches.Patch(color='#DDDDDD', label='Do not ship')]
    ax.legend(handles=patches, fontsize=8, loc='lower right')
    plt.tight_layout()
    st.pyplot(fig)

else:
    r = next(x for x in results if f"Exp {x['id']} — {x['name']}" == page)
    ship  = r["ship"]
    color = GREEN if ship else RED
    rec_class = "rec-ship" if ship else "rec-hold"
    verdict_text = "Recommended to Ship" if ship else "Do Not Ship"
    verdict_icon = "✓" if ship else "✗"

    st.markdown(f"""
    <div class="story-block" style="border-top: 3px solid {color}; padding-top: 28px;">
        <div style="display:flex; justify-content:space-between; align-items:flex-start; flex-wrap:wrap; gap:16px;">
            <div>
                <div class="section-label">Experiment {r['id']} of 4</div>
                <h2 style="margin:0 0 6px 0; font-size:1.6rem;">{r['name']}</h2>
                <div style="font-size:0.85rem; color:#777;">Measuring <strong>{r['metric']}</strong> · {r['test']}</div>
            </div>
            <div style="text-align:right;">
                <span class="verdict-label {'label-ship' if ship else 'label-hold'}" style="font-size:0.85rem; padding:6px 16px;">
                    {verdict_icon} {verdict_text}
                </span>
                <div class="footnote" style="margin-top:8px;">p = {r['p']:.5f} · α = 0.05 · n = 50,000</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="story-block">
        <div class="section-label">What We Tested</div>
        <p style="font-size:0.95rem; line-height:1.8; color:#333; margin:0;">{r['what']}</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div class='story-block'>", unsafe_allow_html=True)
    st.markdown("<div class='section-label'>The Numbers</div>", unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Control",   f"{r['ctrl']:.2f}{r['unit']}")
    c2.metric("Treatment", f"{r['trt']:.2f}{r['unit']}")
    c3.metric("Lift",      f"{r['lift']:+.2f}{r['unit']}", f"{r['lift_pct']:+.1f}% relative")
    c4.metric("p-value",   f"{r['p']:.5f}", "Significant" if ship else "Not significant")
    if r['d'] is not None:
        st.markdown(f"<div class='footnote' style='margin-top:8px;'>Cohen's d = {r['d']:.4f} — {effect_label(r['d'])} practical effect size</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='story-block'>", unsafe_allow_html=True)
    st.markdown("<div class='section-label'>Distribution & Comparison</div>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        fig, ax = plt.subplots(figsize=(6, 3.5))
        if r['id'] == 2:
            vals = [r['ctrl'], r['trt']]
            bars = ax.bar(['Control', 'Treatment'], vals, color=[GREY, color], width=0.4)
            for bar, v in zip(bars, vals):
                ax.text(bar.get_x()+bar.get_width()/2, v+0.05, f'{v:.2f}%',
                        ha='center', fontsize=10, fontweight='600', color='#333', fontfamily='monospace')
            ax.set_ylabel('Click-Through Rate (%)')
            ax.set_title('CTR by group', fontsize=10, color='#444')
        else:
            ax.hist(r['ctrl_data'], bins=60, alpha=0.45, color=GREY,  density=True, label='Control')
            ax.hist(r['trt_data'],  bins=60, alpha=0.65, color=color, density=True, label='Treatment')
            ax.axvline(r['ctrl_data'].mean(), color='#999', linestyle='--', lw=1.5)
            ax.axvline(r['trt_data'].mean(),  color=color,  linestyle='--', lw=1.5)
            ax.set_ylabel('Density')
            ax.set_title('Distribution by group', fontsize=10, color='#444')
            ax.legend(fontsize=8)
        ax.grid(True, alpha=0.4)
        plt.tight_layout()
        st.pyplot(fig)
    with col2:
        fig, ax = plt.subplots(figsize=(6, 3.5))
        means = [r['ctrl'], r['trt']]
        if r['id'] != 2:
            ci_c = ci95(r['ctrl_data']); ci_t = ci95(r['trt_data'])
            errs = [r['ctrl']-ci_c[0], r['trt']-ci_t[0]]
        else:
            errs = [0, 0]
        bars = ax.bar(['Control', 'Treatment'], means, color=[GREY, color], width=0.4, alpha=0.9)
        if r['id'] != 2:
            ax.errorbar(['Control', 'Treatment'], means, yerr=errs, fmt='none', color='#333', capsize=8, lw=1.5)
        for bar, m in zip(bars, means):
            ax.text(bar.get_x()+bar.get_width()/2, m+(max(means)*0.01),
                    f'{m:.2f}{r["unit"]}', ha='center', fontsize=9,
                    fontweight='600', color='#333', fontfamily='monospace')
        ax.set_title('Mean ± 95% CI' if r['id'] != 2 else 'CTR comparison', fontsize=10, color='#444')
        ax.grid(True, axis='y', alpha=0.4)
        plt.tight_layout()
        st.pyplot(fig)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown(f"""
    <div class="story-block">
        <div class="section-label">What Happened</div>
        <p style="font-size:0.95rem; line-height:1.8; color:#333; margin:0 0 20px 0;">{r['result']}</p>
        <div class="recommendation-box {rec_class}">
            <div class="rec-title">Recommendation</div>
            <div class="rec-body">{r['rec']}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div style="padding:16px 20px; background:#F7F6F2; border-radius:4px; margin-top:8px;">
        <div class="section-label" style="margin-bottom:8px;">Statistical Method</div>
        <p style="font-size:0.8rem; color:#777; line-height:1.7; margin:0;">
        <strong>{r['test']}</strong> was used to evaluate this experiment.
        {"A t-test compares the means of two groups to determine whether the observed difference is statistically significant. Welch's variant does not assume equal variance between groups." if r['id'] != 2 else "Chi-Square was used because the outcome (clicked / not clicked) is binary — it tests whether the distribution of clicks differs significantly between groups."}
        The significance threshold is α = 0.05.
        {f"Cohen's d = {r['d']:.4f} ({effect_label(r['d'])} practical effect)." if r['d'] is not None else ""}
        </p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
<div style="border-top:1px solid #E5E5E5; padding-top:16px; display:flex; justify-content:space-between; flex-wrap:wrap; gap:8px;">
    <span style="font-size:0.75rem; color:#aaa; font-family:'IBM Plex Mono',monospace;">TikTok Product Experimentation · Q2 2026 · Synthetic data for portfolio demonstration</span>
    <span style="font-size:0.75rem; color:#aaa; font-family:'IBM Plex Mono',monospace;">Kalpana Joyce Dovari · <a href="https://my-portfolio-taupe-kappa-13.vercel.app/" style="color:#aaa;">Portfolio</a> · <a href="https://github.com/kalpanajoycedovari" style="color:#aaa;">GitHub</a></span>
</div>
""", unsafe_allow_html=True)