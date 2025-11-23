import pandas as pd

def statistical_parity(df, sensitive, label="decision"):
    if sensitive not in df.columns or label not in df.columns:
        return float('nan')
    col = df[label].apply(lambda x: 1 if str(x).lower() in ("1","true","approved","yes") else 0)
    groups = df[sensitive].unique()
    if len(groups) < 2:
        return float('nan')
    g0 = df[df[sensitive] == groups[0]]
    g1 = df[df[sensitive] == groups[1]]
    if len(g0) == 0 or len(g1) == 0:
        return float('nan')
    return float(g0[label].apply(lambda x: 1 if str(x).lower() in ("1","true","approved","yes") else 0).mean()
                 - g1[label].apply(lambda x: 1 if str(x).lower() in ("1","true","approved","yes") else 0).mean())
