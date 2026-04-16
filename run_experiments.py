import time
import random
import argparse
import numpy as np
import matplotlib.pyplot as plt


# ──────────────────────────────────────────────
#  Sorting Algorithms
# ──────────────────────────────────────────────

def bubble_sort(arr):
    a = arr.copy()
    n = len(a)
    for i in range(n):
        for j in range(0, n - i - 1):
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
    return a


def selection_sort(arr):
    a = arr.copy()
    n = len(a)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if a[j] < a[min_idx]:
                min_idx = j
        a[i], a[min_idx] = a[min_idx], a[i]
    return a


def insertion_sort(arr):
    a = arr.copy()
    for i in range(1, len(a)):
        key = a[i]
        j = i - 1
        while j >= 0 and a[j] > key:
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = key
    return a


def merge_sort(arr):
    if len(arr) <= 1:
        return arr.copy()
    mid   = len(arr) // 2
    left  = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return _merge(left, right)


def _merge(left, right):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i]); i += 1
        else:
            result.append(right[j]); j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result


def quick_sort(arr):
    a = arr.copy()
    _quick_sort_inplace(a, 0, len(a) - 1)
    return a


def _quick_sort_inplace(a, low, high):
    if low < high:
        pi = _partition(a, low, high)
        _quick_sort_inplace(a, low, pi - 1)
        _quick_sort_inplace(a, pi + 1, high)


def _median_of_five(a, low, high):
    step = max(1, (high - low) // 4)
    candidates = [low, low + step, (low + high) // 2, high - step, high]
    candidates = [max(low, min(high, c)) for c in candidates]
    
    for i in range(1, 5):
        key_val = a[candidates[i]]
        key_idx = candidates[i]
        j = i - 1
        while j >= 0 and a[candidates[j]] > key_val:
            candidates[j + 1] = candidates[j]
            j -= 1
        candidates[j + 1] = key_idx
    
    return candidates[2]  


def _partition(a, low, high):
    if high - low >= 4:
        median_idx = _median_of_five(a, low, high)
        a[median_idx], a[high] = a[high], a[median_idx]   
    pivot = a[high]
    i = low - 1
    for j in range(low, high):
        if a[j] <= pivot:
            i += 1
            a[i], a[j] = a[j], a[i]
    a[i + 1], a[high] = a[high], a[i + 1]
    return i + 1


# ── Algorithm registry ─────────────────────────
ALGORITHMS = {
    1: ("Bubble Sort",    bubble_sort),
    2: ("Selection Sort", selection_sort),
    3: ("Insertion Sort", insertion_sort),
    4: ("Merge Sort",     merge_sort),
    5: ("Quick Sort",     quick_sort),
}

SLOW_ALGOS = {"Bubble Sort", "Selection Sort", "Insertion Sort"}
SLOW_LIMIT  = 20_000   

COLORS = {
    "Bubble Sort":    "#e74c3c",
    "Selection Sort": "#e67e22",
    "Insertion Sort": "#3498db",
    "Merge Sort":     "#2ecc71",
    "Quick Sort":     "#9b59b6",
}


# ──────────────────────────────────────────────
#  Array Generators
# ──────────────────────────────────────────────

def random_array(n):
    return [random.randint(0, 10 * n) for _ in range(n)]


def nearly_sorted_array(n, noise_fraction):
    arr = list(range(n))
    num_swaps = max(1, int(n * noise_fraction))
    for _ in range(num_swaps):
        i, j = random.randint(0, n - 1), random.randint(0, n - 1)
        arr[i], arr[j] = arr[j], arr[i]
    return arr


# ──────────────────────────────────────────────
#  Timing
# ──────────────────────────────────────────────

def measure(sort_fn, arr):
    start = time.perf_counter()
    sort_fn(arr)
    return time.perf_counter() - start


def run_experiment(algo_ids, sizes, repetitions, array_gen):
    """Returns  { algo_name: { size: (mean, std) } }"""
    results = {}
    for aid in algo_ids:
        if aid not in ALGORITHMS:
            print(f"  [!] Unknown algorithm ID {aid} – skipping.")
            continue
        name, fn = ALGORITHMS[aid]
        results[name] = {}
        for n in sizes:
            if name in SLOW_ALGOS and n > SLOW_LIMIT:
                results[name][n] = (float("nan"), float("nan"))
                print(f"  {name:15s}  n={n:>9,}  [skipped – too slow]")
                continue
            times = [measure(fn, array_gen(n)) for _ in range(repetitions)]
            mean, std = np.mean(times), np.std(times)
            results[name][n] = (mean, std)
            print(f"  {name:15s}  n={n:>9,}  mean={mean:.4f}s  std={std:.4f}s")
    return results


# ──────────────────────────────────────────────
#  Plotting
# ──────────────────────────────────────────────

def plot_results(results, sizes, title, filename):
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.set_facecolor("#f8f9fa")
    fig.patch.set_facecolor("white")
    ax.grid(True, linestyle="--", alpha=0.5, color="#cccccc")

    for name, size_data in results.items():
        color = COLORS.get(name, "gray")
        xs    = np.array(sizes, dtype=float)
        means = np.array([size_data.get(n, (float("nan"), float("nan")))[0] for n in sizes])
        stds  = np.array([size_data.get(n, (float("nan"), float("nan")))[1] for n in sizes])

        mask = ~np.isnan(means)
        ax.plot(xs[mask], means[mask], marker="o", label=name,
                color=color, linewidth=2, markersize=5)
        ax.fill_between(xs[mask],
                        (means - stds)[mask],
                        (means + stds)[mask],
                        alpha=0.15, color=color)

    ax.set_xlabel("Array size (n)", fontsize=12)
    ax.set_ylabel("Runtime (seconds)", fontsize=12)
    ax.set_title(title, fontsize=14, fontweight="bold")
    ax.legend(fontsize=11)
    plt.tight_layout()
    plt.savefig(filename, dpi=150)
    plt.close()
    print(f"  Saved → {filename}")


# ──────────────────────────────────────────────
#  CLI  (Part D)
#
#  Example (from assignment):
#    python run_experiments.py -a 1 2 5 -s 100 500 3000 -e 1 -r 20
# ──────────────────────────────────────────────

def parse_args():
    parser = argparse.ArgumentParser(
        description="Sorting Algorithm Benchmark",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "-a", nargs="+", type=int, default=[1, 3, 4],
        metavar="ID",
        help=(
            "Algorithm IDs to compare (space-separated):\n"
            "  1 = Bubble Sort\n"
            "  2 = Selection Sort\n"
            "  3 = Insertion Sort\n"
            "  4 = Merge Sort\n"
            "  5 = Quick Sort\n"
            "Example: -a 1 2 5"
        )
    )
    parser.add_argument(
        "-s", nargs="+", type=int,
        default=[100, 500, 1000, 5000, 10000],
        metavar="N",
        help=(
            "Array sizes to benchmark (space-separated).\n"
            "Example: -s 100 500 3000"
        )
    )
    parser.add_argument(
        "-e", type=int, default=0,
        choices=[0, 1, 2],
        help=(
            "Experiment type / noise level:\n"
            "  0 = Random arrays – saves result1.png  [default]\n"
            "  1 = Nearly sorted, 5%% noise – saves result2.png\n"
            "  2 = Nearly sorted, 20%% noise – saves result2.png"
        )
    )
    parser.add_argument(
        "-r", type=int, default=5,
        metavar="R",
        help="Number of repetitions per array size. Default: 5"
    )
    return parser.parse_args()


# ──────────────────────────────────────────────
#  Main
# ──────────────────────────────────────────────

def main():
    args = parse_args()

    algo_names = [ALGORITHMS[i][0] for i in args.a if i in ALGORITHMS]
    print("\n=== Sorting Algorithm Benchmark ===")
    print(f"  Algorithms  : {algo_names}")
    print(f"  Sizes       : {args.s}")
    print(f"  Experiment  : {args.e}")
    print(f"  Repetitions : {args.r}\n")

    if args.e == 0:
        # ── Part B – Random arrays ──────────────
        print("── Part B: Random Arrays ──")
        results = run_experiment(args.a, args.s, args.r, random_array)
        plot_results(results, args.s,
                     title="Runtime Comparison (Random Arrays)",
                     filename="result1.png")

    else:
        # ── Part C – Nearly sorted arrays ───────
        noise     = 0.05 if args.e == 1 else 0.20
        noise_pct = int(noise * 100)
        label     = f"Nearly Sorted (noise={noise_pct}%)"
        print(f"── Part C: {label} ──")
        results = run_experiment(args.a, args.s, args.r,
                                 lambda n: nearly_sorted_array(n, noise))
        plot_results(results, args.s,
                     title=f"Runtime Comparison ({label})",
                     filename="result2.png")

    print("\nDone!")


if __name__ == "__main__":
    main()
