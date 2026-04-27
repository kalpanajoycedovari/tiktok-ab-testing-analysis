# TikTok A/B Testing Analysis

A simulation of the kind of experimentation work that runs quietly behind every product decision at companies like TikTok, YouTube, and Meta. Four concurrent experiments, 50,000 users, real statistical methods.

---

## What this is

Product teams at large platforms don't ship features because someone had a good feeling. They run controlled experiments, measure the effect on a specific metric, and make the call based on evidence. This project simulates exactly that — a Q2 experiment suite testing four separate product changes simultaneously, the way a real data analyst would handle it.

The analysis covers the full workflow: define the hypothesis, split users into control and treatment groups, run the appropriate statistical test, measure effect size, and write a clear recommendation. Two experiments show a real effect. Two don't. That's intentional — in practice, most experiments fail to move the metric they target, and knowing when *not* to ship is just as important as knowing when to.

---

## The dataset

The data is synthetic, generated using Python's NumPy library. This is the honest and correct approach — TikTok's internal user data is proprietary and never publicly released. The distributions were calibrated against publicly reported industry benchmarks:

- Average TikTok session length: ~10 minutes
- Typical video completion rate: 50–60%
- Feed click-through rate: 3–6%
- Daily app opens for active users: 8–10

**Normal distribution** was used for continuous metrics like watch time and session length — human behaviour naturally clusters around a mean with variance either side. **Binomial distribution** was used for binary outcomes like clicks — the result is either 0 or 1, and the probability parameter was set to match real-world CTR benchmarks.

The final dataset has 50,000 rows and 13 columns, covering user demographics (age, country, device, tenure) and experiment assignments and outcome metrics for all four experiments.

---

## The four experiments

**Experiment 1 — Recommendation Algorithm**
Tests whether a new For You feed ranking model increases average watch time per video. Measured using Welch's T-Test. Result: significant — the algorithm lifted watch time by ~12 seconds on average.

**Experiment 2 — Thumbnail Format**
Tests whether a larger thumbnail format increases click-through rate. CTR is a binary outcome (clicked or not), so Chi-Square was used instead of a T-Test. Result: significant — CTR improved from ~4% to ~5.8%.

**Experiment 3 — Notification Timing**
Tests whether changing the push notification send time increases daily app opens. Result: not significant — both groups were virtually identical. Do not ship.

**Experiment 4 — Autoplay Toggle**
Tests whether enabling autoplay by default extends session length. Result: not significant — no detectable effect. Do not ship.

---

## Why these statistical tests

**Welch's T-Test** compares the means of two groups. The Welch variant is used specifically because it does not assume equal variance between control and treatment — a safer assumption in real experiments where group characteristics may differ slightly. It answers the question: is this difference real, or is it just noise?

**Chi-Square Test** is used when the outcome is categorical rather than continuous. For CTR, a user either clicked or didn't — there's no mean to compare. Chi-Square tests whether the distribution of clicks differs significantly between the two groups.

**Cohen's d** measures practical effect size alongside the p-value. A result can be statistically significant but so small it makes no difference in the real world. Cohen's d gives you a second check: is this effect actually worth caring about?

**p-value threshold: 0.05** — meaning there's less than a 5% probability the observed result happened by chance before concluding the treatment had a real effect.

---

## What sets this apart

Most portfolio A/B testing projects run one experiment on a Kaggle dataset and call it done. This one:

- Runs four experiments simultaneously, the way real platforms operate
- Deliberately includes two null results — because real experimentation suites don't produce significant findings every time
- Uses the correct test for each metric type rather than applying T-Test to everything
- Computes effect size, not just significance
- Presents findings in a stakeholder dashboard written in plain English — verdicts, recommendations, and business context — not just p-values

The Streamlit dashboard was designed to be readable by a product manager or CEO, not just a data scientist.

---

---

## Running it locally

```bash
git clone https://github.com/kalpanajoycedovari/tiktok-ab-testing-analysis
cd tiktok-ab-testing-analysis
pip install -r requirements.txt
python data/generate_data.py
streamlit run streamlit_app/app.py
```

---

## Live demo

[tiktok-ab-testing-analysis.streamlit.app](https://tiktok-ab-testing-analysis.streamlit.app)

---

## Author

Kalpana Joyce Dovari — MSc Artificial Intelligence, Northumbria University London  
[Portfolio](https://my-portfolio-taupe-kappa-13.vercel.app) · [GitHub](https://github.com/kalpanajoycedovari) · [LinkedIn](https://linkedin.com/in/kalpanajoycedovari)
