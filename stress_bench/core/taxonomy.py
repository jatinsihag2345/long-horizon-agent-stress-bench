from enum import Enum
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from datetime import datetime


class FailureCategory(str, Enum):
    CONTEXT_WINDOW_DRIFT = "Context Window Drift"       # Forgets initial constraints after turn 10
    CIRCULAR_RETRY_LOOP = "Circular Retry Loop"         # Repeats identical failing command >= 3 times
    STATE_DESYNCHRONIZATION = "State Desynchronization" # Operates on stale assumptions without inspecting exit codes
    TOOL_HALLUCINATION = "Tool Hallucination"           # Passes invalid flags/parameters not supported by environment
    BACKTRACKING_PARALYSIS = "Backtracking Paralysis"   # Refuses to rollback bad mutations, enters deeper corruption
    PREMATURE_TERMINATION = "Premature Termination"     # Emits completion signal without verifying task invariants


class FailureSeverity(str, Enum):
    BENIGN = "Benign"       # Recoverable in subsequent steps with minor token waste
    DEGRADATION = "Degradation" # Sub-optimal trajectory, increased latency/cost
    CATASTROPHIC = "Catastrophic" # Permanent task failure, corrupted environment state


@dataclass
class FailureInstance:
    category: FailureCategory
    severity: FailureSeverity
    step_number: int
    command: str
    error_context: str
    explanation: str


@dataclass
class TrajectoryEvaluation:
    task_id: str
    agent_id: str
    total_steps: int
    goal_achieved: bool
    constraints_violated: int
    score: float  # 0.0 to 1.0 (penalized by constraint violations and step waste)
    failures: List[FailureInstance] = field(default_factory=list)
    timestamp: datetime = field(default_factory=datetime.utcnow)
