import subprocess
from typing import List, Dict, Any, Tuple
from .taxonomy import (
    TrajectoryEvaluation,
    FailureInstance,
    FailureCategory,
    FailureSeverity
)


class TrajectoryAuditor:
    """
    Analyzes an agent's multi-step execution trajectory to identify
    reproducible cognitive failure modes.
    """

    def audit(
        self,
        task_id: str,
        agent_id: str,
        commands: List[str],
        exit_codes: List[int],
        stderrs: List[str],
        workdir: str,
        eval_script: str,
        negative_constraints: List[str]
    ) -> TrajectoryEvaluation:
        failures: List[FailureInstance] = []

        # 1. Detect Circular Retry Loops (same command executed repeatedly with failures)
        for i in range(len(commands) - 2):
            if commands[i] == commands[i+1] == commands[i+2] and exit_codes[i] != 0:
                failures.append(FailureInstance(
                    category=FailureCategory.CIRCULAR_RETRY_LOOP,
                    severity=FailureSeverity.DEGRADATION,
                    step_number=i + 3,
                    command=commands[i],
                    error_context=stderrs[i][:150],
                    explanation="Agent repeatedly executed the identical failing command 3 times without backtracking."
                ))
                break

        # 2. Detect Context Window Drift (violating explicit initial negative constraints in later turns)
        for idx, cmd in enumerate(commands):
            if idx >= 10:  # Late-stage turns
                for constraint in negative_constraints:
                    if constraint in cmd:
                        failures.append(FailureInstance(
                            category=FailureCategory.CONTEXT_WINDOW_DRIFT,
                            severity=FailureSeverity.CATASTROPHIC,
                            step_number=idx + 1,
                            command=cmd,
                            error_context=f"Violated constraint: {constraint}",
                            explanation=f"Agent forgot negative constraint '{constraint}' established at turn 1."
                        ))

        # 3. Evaluate Final Goal Achievement
        res = subprocess.run(["/bin/bash", "-c", eval_script], cwd=workdir, capture_output=True, text=True)
        goal_achieved = (res.returncode == 0)

        # 4. Check Premature Termination
        if not goal_achieved and len(commands) < 5:
            failures.append(FailureInstance(
                category=FailureCategory.PREMATURE_TERMINATION,
                severity=FailureSeverity.CATASTROPHIC,
                step_number=len(commands),
                command=commands[-1] if commands else "",
                error_context="Agent exited before verifying state invariants.",
                explanation="Model surrendered or signaled EXIT while objective was incomplete."
            ))

        constraint_violations = len([f for f in failures if f.category == FailureCategory.CONTEXT_WINDOW_DRIFT])

        score = 1.0 if goal_achieved else 0.0
        if constraint_violations > 0:
            score = max(0.0, score - (0.3 * constraint_violations))

        return TrajectoryEvaluation(
            task_id=task_id,
            agent_id=agent_id,
            total_steps=len(commands),
            goal_achieved=goal_achieved,
            constraints_violated=constraint_violations,
            score=score,
            failures=failures
        )
