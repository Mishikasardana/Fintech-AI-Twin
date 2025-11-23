class LLMClient:
    def __init__(self):
        pass

    def generate(self, prompt: str):
        # Simple fallback: extract bullets if present
        if "Attribution bullets:" in prompt:
            bullets = prompt.split("Attribution bullets:")[1].strip()
            lines = [l.strip().lstrip("-").strip() for l in bullets.splitlines() if l.strip()]
            if not lines:
                return "We examined your application. Key model factors are returned above."
            text = "It looks like the main factors affecting the decision are: " + "; ".join(lines[:3]) + "."
            text += " Consider improving these factors or contacting support to appeal."
            return text
        return "We examined your application. The top factors are listed in the response."
