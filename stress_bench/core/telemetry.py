from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class TrajectoryCostEstimate:
    total_tokens: int
    prompt_tokens: int
    completion_tokens: int
    estimated_cost_usd: float
    cost_per_step_usd: float


class StepCostEstimator:
    """
    Computes economic cost metrics for long-horizon agent trajectories
    using standard frontier pricing models ($3.00/1M prompt, $15.00/1M completion).
    """

    def __init__(self, prompt_price_per_m: float = 3.0, completion_price_per_m: float = 15.0):
        self.prompt_price_per_m = prompt_price_per_m
        self.completion_price_per_m = completion_price_per_m

    def estimate(self, prompt_tokens: int, completion_tokens: int, steps: int) -> TrajectoryCostEstimate:
        prompt_cost = (prompt_tokens / 1_000_000.0) * self.prompt_price_per_m
        completion_cost = (completion_tokens / 1_000_000.0) * self.completion_price_per_m
        total_cost = round(prompt_cost + completion_cost, 4)
        cost_per_step = round(total_cost / steps, 4) if steps > 0 else 0.0

        return TrajectoryCostEstimate(
            total_tokens=prompt_tokens + completion_tokens,
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            estimated_cost_usd=total_cost,
            cost_per_step_usd=cost_per_step
        )
