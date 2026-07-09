"""Cliente de inferencia mock (determinista, sin red).

En producción, esto invoca a Amazon Bedrock (o SageMaker) con el modelo ruteado.
"""

from __future__ import annotations

from dataclasses import dataclass


def _estimate_tokens(text: str) -> int:
    return max(1, len(text or "") // 4)


@dataclass
class Inference:
    text: str
    model: str
    input_tokens: int
    output_tokens: int


class MockInference:
    def complete(self, model: str, prompt: str) -> Inference:
        answer = f"[{model}] respuesta a: {(prompt or '').strip()[:80]}"
        return Inference(
            text=answer,
            model=model,
            input_tokens=_estimate_tokens(prompt),
            output_tokens=_estimate_tokens(answer),
        )
