#!/usr/bin/env python3
import subprocess
import sys
import re
import random
import matplotlib.pyplot as plt


def generate_test_input(n, min_power=0, max_power=99999999):
    """Generate a random test case with n amino acids"""
    powers = [random.randint(min_power, max_power) for _ in range(n)]
    classes = "".join(random.choice("PNAB") for _ in range(n))

    return f"{n}\n{' '.join(map(str, powers))}\n{classes}\n"


def run_single_test(project, n, max_power):
    """Run a single test and measure execution time"""
    test_input = generate_test_input(n, 0, max_power)

    cmd = [f"./{project}"]
    result = subprocess.run(
        cmd, input=test_input, capture_output=True, text=True, timeout=60
    )

    # Get execution time from /usr/bin/time or measure it ourselves
    import time

    start = time.time()
    result = subprocess.run(
        cmd, input=test_input, capture_output=True, text=True, timeout=60
    )
    elapsed = time.time() - start

    return elapsed


def run_tests(project, pmax, n_start, N_max, repetitions, seed=None):
    """Run multiple tests with increasing N"""
    if seed is not None:
        random.seed(seed)

    n_values = []
    times = []

    current_n = n_start
    for i in range(repetitions):
        print(f"Test {i} (N={current_n})...", end=" ", flush=True)
        try:
            n_avg = 5  # maybe change to args
            total = 0
            for i2 in range(n_avg):
                total += run_single_test(project, current_n, pmax)
            elapsed = total / n_avg
            n_values.append(current_n**3)
            times.append(elapsed)
            print(f"{elapsed:.3f}s")
        except subprocess.TimeoutExpired:
            print("TIMEOUT")
            break
        except Exception as e:
            print(f"ERROR: {e}")
            break
        current_n = n_start + round(
            (((N_max**3) - (n_start**3)) * (i + 1) / (repetitions - 1)) ** (1 / 3)
        )

    return n_values, times


def plot_results(n_values, times, project):
    """Create a plot of N vs execution time and a table"""
    fig, (ax1, ax2) = plt.subplots(
        2, 1, figsize=(10, 10), gridspec_kw={"height_ratios": [2, 1]}
    )

    # Plot
    ax1.plot(n_values, times, "bo-", linewidth=2, markersize=8)
    ax1.set_xlabel("n³", fontsize=12)
    ax1.set_ylabel("Tempo (s)", fontsize=12)
    ax1.set_title(f"Análise experimental", fontsize=14)
    ax1.grid(True, alpha=0.3)

    # Add value labels on points
    for n, t in zip(n_values, times):
        ax1.annotate(
            f"{t:.3f}s",
            (n, t),
            textcoords="offset points",
            xytext=(0, 10),
            ha="center",
            fontsize=9,
        )

    # Table
    n_list = [int(n3 ** (1 / 3)) for n3 in n_values]
    table_data = [[n, n2, f"{t:.4f}"] for n, n2, t in zip(n_list, n_values, times)]

    ax2.axis("tight")
    ax2.axis("off")
    table = ax2.table(
        cellText=table_data,
        colLabels=["N", "N³", "Tempo (s)"],
        cellLoc="center",
        loc="center",
        colWidths=[0.3, 0.3, 0.3],
    )
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1, 2)

    # Style header
    for i in range(3):
        table[(0, i)].set_facecolor("#4CAF50")
        table[(0, i)].set_text_props(weight="bold", color="white")

    # Alternate row colors
    for i in range(1, len(table_data) + 1):
        for j in range(3):
            if i % 2 == 0:
                table[(i, j)].set_facecolor("#f0f0f0")

    plt.tight_layout()
    plt.savefig(f"{project}_performance.png", dpi=150)
    print(f"Graph saved as '{project}_performance.png'")
    plt.show()


if __name__ == "__main__":
    if len(sys.argv) < 6:
        print(
            "Usage: python3 perf.py <project> <Pmax> <N_start> <N_max> <repetitions> [seed]"
        )
        print("Example: python3 perf.py projeto 99999 100 100 10")
        sys.exit(1)

    project = sys.argv[1]
    pmax = int(sys.argv[2])
    n_start = int(sys.argv[3])
    N_max = int(sys.argv[4])
    repetitions = int(sys.argv[5])
    seed = int(sys.argv[6]) if len(sys.argv) > 6 else None

    print(f"Running performance tests for {project}...")
    print(f"Starting N={n_start}, increment={N_max}, repetitions={repetitions}")
    print("---")

    n_values, times = run_tests(project, pmax, n_start, N_max, repetitions, seed)

    if not n_values:
        print("ERROR: No timing data collected")
        sys.exit(1)

    for i in range(len(n_values)):
        print(f"N={n_values[i]}, N^2={n_values[i] ** 3}, tempo={times[i]}")
    print("[")
    for i in range(len(n_values)):
        print(f"[ {n_values[i]}, {n_values[i] ** 3}, {times[i]} ]")
    print("]")
    print("N values:", n_values)
    print("Times:", [f"{t:.3f}" for t in times])

    plot_results(n_values, times, project)
