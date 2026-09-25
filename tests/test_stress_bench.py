from stress_bench.tasks.long_horizon_tasks import ALL_LONG_HORIZON_TASKS
from stress_bench.core.evaluator import TrajectoryAuditor
from stress_bench.core.taxonomy import FailureCategory


def test_tasks_defined():
    assert len(ALL_LONG_HORIZON_TASKS) >= 2
    for t in ALL_LONG_HORIZON_TASKS:
        assert t.id.startswith("task_lh_")
        assert len(t.negative_constraints) > 0


def test_circular_loop_detection():
    auditor = TrajectoryAuditor()
    commands = ["cat missing.txt", "cat missing.txt", "cat missing.txt"]
    exit_codes = [1, 1, 1]
    stderrs = ["No such file", "No such file", "No such file"]

    res = auditor.audit(
        task_id="test_mock",
        agent_id="FailingAgent",
        commands=commands,
        exit_codes=exit_codes,
        stderrs=stderrs,
        workdir="/tmp",
        eval_script="exit 1",
        negative_constraints=[]
    )
    assert any(f.category == FailureCategory.CIRCULAR_RETRY_LOOP for f in res.failures)
