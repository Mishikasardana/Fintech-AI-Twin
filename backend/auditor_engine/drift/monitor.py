import numpy as np

def kl_divergence(p, q):
    p = p + 1e-9
    q = q + 1e-9
    return (p * np.log(p / q)).sum()

def detect_drift(df):
    numeric_cols = df.select_dtypes(include=['int','float']).columns
    if len(numeric_cols) == 0:
        return 0.0
    scores = []
    for c in numeric_cols:
        vals = df[c].dropna().values
        if len(vals) < 2:
            continue
        hist, _ = np.histogram(vals, bins=5, density=True)
        uniform = np.ones_like(hist) / len(hist)
        scores.append(kl_divergence(hist, uniform))
    return float(sum(scores) / max(1, len(scores)))
