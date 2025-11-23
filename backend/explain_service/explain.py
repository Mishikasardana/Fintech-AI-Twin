import pandas as pd
from typing import Dict, List, Tuple
from .model import DummyCreditModel
from .llm_client import LLMClient

_model = None
_llm = None

def get_model():
    global _model
    if _model is None:
        _model = DummyCreditModel()
    return _model

def compute_shap_attributions(input_row: Dict) -> List[Tuple[str, float]]:
    model = get_model()
    df = pd.DataFrame([input_row])
    vals, features = model.shap_values(df)
    row = vals[0]
    pairs = list(zip(features, [float(v) for v in row]))
    pairs_sorted = sorted(pairs, key=lambda x: abs(x[1]), reverse=True)
    return pairs_sorted

def build_template(attributions, top_k=3):
    lines = []
    for feat, v in attributions[:top_k]:
        if v < 0:
            lines.append(f"- {feat.replace('_',' ').title()} likely contributed negatively to the decision.")
        else:
            lines.append(f"- {feat.replace('_',' ').title()} was supportive of approval.")
    return "Attribution bullets:\n" + "\n".join(lines)

def nl_explanation(attributions, context=None):
    global _llm
    if _llm is None:
        _llm = LLMClient()
    template = build_template(attributions, top_k=4)
    prompt = f"""You are an empathetic assistant. Convert the concise model attribution bullets into a simple customer-facing explanation.

Context: {context or {}}

Attribution bullets:
{template}
"""
    return _llm.generate(prompt)
