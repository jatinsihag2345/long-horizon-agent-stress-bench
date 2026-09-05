import tempfile
import os
import shutil
import subprocess
from typing import Tuple, List, Dict, Any


class StatefulEnvironment:
    """
    Manages an isolated directory environment and monitors agent behavior for
    anti-patterns (circular commands, excessive failures, constraint violations).
    """

    def __init__(self, task_id: str, constraints: List[str]):
        self.task_id = task_id
        self.constraints = constraints
        self.workdir: str = tempfile.mkdtemp(prefix=f"lh_bench_{task_id}_")
        self.history: List[str] = []

    def setup(self, setup_script: str):
        script_file = os.path.join(self.workdir, "_setup.sh")
        with open(script_file, "w") as f:
            f.write("#!/bin/bash\nset -e\n" + setup_script)
        os.chmod(script_file, 0o755)
        res = subprocess.run(["/bin/bash", script_file], cwd=self.workdir, capture_output=True, text=True)
        return res.returncode == 0

    def step(self, command: str) -> Tuple[int, str, str]:
        self.history.append(command.strip())
        res = subprocess.run(
            ["/bin/bash", "-c", command],
            cwd=self.workdir,
            capture_output=True,
            text=True,
            timeout=30
        )
        return res.returncode, res.stdout, res.stderr

    def teardown(self):
        if os.path.exists(self.workdir):
            shutil.rmtree(self.workdir, ignore_errors=True)
