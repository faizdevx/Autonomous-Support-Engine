from scripts.simulate import run_simulation, write_outputs


if __name__ == "__main__":
    rows, summary = run_simulation()
    write_outputs(rows, summary)
    print(f"Simulation runs: {summary.runs}")
    print(f"Resolution rate: {summary.resolution_rate:.2%}")
    print(f"Escalation rate: {summary.escalation_rate:.2%}")
