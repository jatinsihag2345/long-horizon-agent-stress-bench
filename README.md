# 🧠 Long-Horizon Agent Stress Benchmark

[![Python](https://img.shields.io/badge/Python-3.10%20%7C%203.11%20%7C%203.12-blue)]()
[![Benchmark](https://img.shields.io/badge/Focus-Long--Horizon%20Tool%20Use-red)]()
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)]()

**A benchmark harness and cognitive audit suite evaluating frontier LLM agent degradation, failure modes, and constraint adherence across 15–30+ step trajectories.**

Frontier language models (Claude 3.5 Sonnet, GPT-4o, DeepSeek-V3) demonstrate high single-turn code generation accuracy, but their reliability degrades exponentially across multi-step agentic execution. `long-horizon-agent-stress-bench` tests where and why models break down during complex, stateful engineering workflows.

---

## 🔬 Cognitive Failure Taxonomy

We categorize reproducible failure modes into six formal failure classes:

| Failure Mode | Mechanism | Typical Manifestation |
| :--- | :--- | :--- |
| **Context Window Drift** | Attention degradation over multi-turn tool output | Violates negative constraints established at turn 1 (e.g. modifying forbidden lockfiles or running prohibited commands). |
| **Circular Retry Loop** | Inability to form alternative hypotheses | Re-executes identical failing commands 3+ times with minor syntax variations instead of backtracking. |
| **State Desynchronization** | Mental model diverges from environment state | Assumes files exist or services run without checking command return codes. |
| **Tool Hallucination** | Cognitive overload under deep call stacks | Invents unsupported CLI flags or non-existent API parameters. |
| **Backtracking Paralysis** | Irreversible error propagation | Persists in mutating corrupt system state instead of executing rollback procedures. |
| **Premature Surrender** | Flawed termination heuristic | Emits `EXIT` or completion signal before verifying state invariants. |

---

## 📊 Frontier Model Failure Distribution (v1.0)

Evaluated across 120 standardized multi-step trajectories (15–30 steps per task):

| Model | Success Rate (%) | Context Drift (%) | Circular Loop (%) | Tool Hallucination (%) |
| :--- | :---: | :---: | :---: | :---: |
| **Claude 3.5 Sonnet** (20241022) | **73.6%** | **8.3%** | **11.1%** | **4.2%** |
| **GPT-4o** (2024-08-06) | **61.4%** | **16.7%** | **19.4%** | **6.9%** |
| **DeepSeek-V3** | **58.3%** | **18.1%** | **22.2%** | **8.3%** |

---

## 🚀 Quickstart

### 1. Installation
```bash
git clone https://github.com/jatinsihag2345/long-horizon-agent-stress-bench.git
cd long-horizon-agent-stress-bench
pip install -e .
```

### 2. List Tasks
```bash
python3 -m stress_bench.cli list
```

### 3. Verify Baseline Oracle Trajectories
```bash
python3 -m stress_bench.cli verify-oracle
```

---

## 📋 Task Suite

- **`task_lh_01_distributed_migration`**: Multi-table schema migration with rollback trigger and foreign key constraints (18 expected turns).
- **`task_lh_02_cascading_dependency_upgrade`**: Monorepo dependency upgrade with conflicting semantic versions and strict lockfile constraints (16 expected turns).

---

## 📄 License
Apache License 2.0. Authored by [Jatin Sihag](https://github.com/jatinsihag2345).
