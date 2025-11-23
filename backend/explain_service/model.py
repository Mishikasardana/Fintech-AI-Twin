# explain_service/model.py
import numpy as np
import pandas as pd

class DummyCreditModel:
    def __init__(self):
        self.feature_names = ["income", "age", "credit_score", "spending_ratio"]

    def predict(self, X: pd.DataFrame):
        decisions = []
        for _, row in X.iterrows():
            score = (
                0.4 * (row["income"] / 100000) +
                0.3 * (row["credit_score"] / 900) -
                0.3 * row["spending_ratio"]
            )
            decisions.append("approved" if score > 0.5 else "denied")
        return decisions

    def shap_values(self, X: pd.DataFrame):
        shap = np.random.uniform(-1, 1, (len(X), len(self.feature_names)))
        return shap, self.feature_names
