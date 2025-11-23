import pandas as pd

class WhatIfEngine:
    def __init__(self, model):
        self.model = model

    def search_counterfactuals(self, input_data: dict):
        df = pd.DataFrame([input_data])
        original_pred = self.model.predict(df)[0]

        counterfactuals = []

        # Extended ranges to ensure a flip
        search_space = {
            "income": range(0, 300000, 5000),        # up to 3 lakh
            "credit_score": range(-200, 400, 20),     # explore negative & positive shifts
            "spending_ratio": [-0.70, -0.60, -0.50, -0.40, -0.30, -0.20, -0.10],
            "age": range(-5, 15, 2)                   # age shifts
        }

        for feature, adjustments in search_space.items():
            for adj in adjustments:
                new = input_data.copy()

                # SPECIAL CASES
                if feature == "spending_ratio":
                    new_value = new[feature] + adj
                    if new_value <= 0: 
                        new_value = 0.01
                    new[feature] = new_value
                else:
                    new_value = new[feature] + adj
                    if new_value < 0:
                        new_value = 0
                    new[feature] = new_value

                df_new = pd.DataFrame([new])
                new_pred = self.model.predict(df_new)[0]

                if new_pred != original_pred:
                    counterfactuals.append({
                        "changed_feature": feature,
                        "change": adj,
                        "new_input": new,
                        "new_prediction": new_pred
                    })
                    break   # stop searching further for this feature

        return counterfactuals
