from ..core.taxonomy import TrajectoryEvaluation


def render_ascii_report(eval_res: TrajectoryEvaluation) -> str:
    lines = [
        f"\n{'='*70}",
        f"TRAJECTORY AUDIT REPORT: {eval_res.task_id} (Agent: {eval_res.agent_id})",
        f"{'='*70}",
        f"Goal Achieved:          {'YES' if eval_res.goal_achieved else 'NO'}",
        f"Total Steps Executed:   {eval_res.total_steps}",
        f"Constraint Violations:  {eval_res.constraints_violated}",
        f"Cognitive Score:        {eval_res.score:.2f} / 1.00",
        f"{'-'*70}",
        f"Detected Cognitive Failures ({len(eval_res.failures)}):"
    ]

    if not eval_res.failures:
        lines.append("  None detected (Clean trajectory)")
    else:
        for idx, f in enumerate(eval_res.failures, 1):
            lines.append(f"  [{idx}] Step {f.step_number}: [{f.severity.value}] {f.category.value}")
            lines.append(f"      Command: {f.command[:60]}")
            lines.append(f"      Details: {f.explanation}")

    lines.append(f"{'='*70}\n")
    return "\n".join(lines)
