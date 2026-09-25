import sys
import argparse
from .tasks.long_horizon_tasks import ALL_LONG_HORIZON_TASKS
from .core.environment import StatefulEnvironment
from .core.evaluator import TrajectoryAuditor
from .visualizer.trajectory_report import render_ascii_report


def list_tasks():
    print(f"\n{'Task ID':<40} {'Expected Steps':<16} {'Constraints'}")
    print("=" * 80)
    for t in ALL_LONG_HORIZON_TASKS:
        print(f"{t.id:<40} {t.expected_steps:<16} {len(t.negative_constraints)}")
    print("=" * 80 + "\n")


def test_reference():
    auditor = TrajectoryAuditor()
    for task in ALL_LONG_HORIZON_TASKS:
        env = StatefulEnvironment(task.id, task.negative_constraints)
        try:
            assert env.setup(task.setup_script)
            commands = []
            exit_codes = []
            stderrs = []
            for cmd in task.reference_solution:
                code, stdout, stderr = env.step(cmd)
                commands.append(cmd)
                exit_codes.append(code)
                stderrs.append(stderr)

            res = auditor.audit(
                task_id=task.id,
                agent_id="OracleReference",
                commands=commands,
                exit_codes=exit_codes,
                stderrs=stderrs,
                workdir=env.workdir,
                eval_script=task.eval_script,
                negative_constraints=task.negative_constraints
            )
            print(render_ascii_report(res))
            if not res.goal_achieved:
                sys.exit(1)
        finally:
            env.teardown()


def main():
    parser = argparse.ArgumentParser(description="Long-Horizon Agent Stress Benchmark")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("list", help="List long-horizon tasks")
    subparsers.add_parser("verify-oracle", help="Verify tasks using reference solutions")

    args = parser.parse_args()
    if args.command == "list":
        list_tasks()
    elif args.command == "verify-oracle":
        test_reference()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
