# Sorting_Assignment

## Student Name
Leon Shumil Kelrikh

## Selected Algorithms
knowing all of those code are highly generic all three was written and only 1 3 and 4 used.
1. **Bubble Sort** (ID: 1) – O(n²) — repeatedly swaps adjacent out-of-order elements until the array is sorted.
2. **Selection Sort** (ID: 2) – O(n²) — finds the minimum element in the unsorted portion and places it at the front.
3. **Insertion Sort** (ID: 3) – O(n²) average, O(n) best case — builds a sorted sub-array one element at a time by inserting each element into its correct position.
4. **Merge Sort** (ID: 4) – O(n log n) — divide-and-conquer algorithm that splits, recursively sorts, and merges.
5. **Quick Sort** (ID: 5) – O(n log n) average — divide-and-conquer using a pivot (median-of-three) to partition the array.

---

## How to Run

Install dependencies (one time only):
```bash
pip3 install numpy matplotlib --break-system-packages
```

### CLI Usage (Part D)

```
python3 run_experiments.py -a <IDs> -s <sizes> -e <experiment> -r <repetitions>
```

| Flag | Description |
|------|-------------|
| `-a` | Algorithm IDs (space-separated): `1`=Bubble, `2`=Selection, `3`=Insertion, `4`=Merge, `5`=Quick |
| `-s` | Array sizes to test (space-separated) |
| `-e` | `0` = Random arrays (result1.png) · `1` = Nearly sorted 5% noise (result2.png) · `2` = Nearly sorted 20% noise (result2.png) |
| `-r` | Number of repetitions per size |

### Example Commands

```bash
# Part B – Random arrays with all algorithms
python3 run_experiments.py -a 1 2 3 4 5 -s 100 500 1000 5000 10000 -e 0 -r 5

# Part C – Nearly sorted, 5% noise (assignment example)
python3 run_experiments.py -a 1 2 5 -s 100 500 3000 -e 1 -r 20

# Part C – Nearly sorted, 20% noise
python3 run_experiments.py -a 1 2 3 4 5 -s 100 500 1000 5000 10000 -e 2 -r 5
```

> **Note:** Bubble Sort, Selection Sort, and Insertion Sort are automatically skipped for array sizes above 20,000 to avoid excessive runtime.

---

## Part B – Random Arrays

![result1](result1.png)

### Explanation
For confirmation check etc/results_in_text.txt to see the written results.

The plot clearly shows the difference between O(n²) and O(n log n) algorithms on random input:

Bubble Sort is the slowest. It takes ~4.06s at n=10,000. Its runtime grows quadratically — going from n=1,000 (~0.033s) to n=10,000 (~4.06s) is roughly a 123× increase for a 10× increase in size, consistent with O(n²).
Insertion Sort is also O(n²) but about 2.4× faster than Bubble Sort in practice (~1.69s at n=10,000 vs ~4.06s). It performs fewer comparisons and writes per pass, but still cannot scale to large inputs.
Merge Sort is dramatically faster, following an O(n log n) growth curve. At n=10,000 it finishes in just ~0.019s — over 200× faster than Bubble Sort at the same size. Its runtime grows very gently even as array size increases.

The shaded bands show one standard deviation across 20 repetitions. Merge Sort has a very tight band, indicating stable and predictable performance. Bubble Sort shows more variance at large sizes due to its sensitivity to element order.

---

## Part C – Nearly Sorted Arrays (5% noise)

![result2](result2.png)

### Explanation – Did runtimes change vs. random input?

On nearly sorted arrays (only 5% of elements are randomly swapped), the runtimes changed noticeably for two of the three algorithms. Comparison is at n=3,000 since that is the largest size tested in Part C:

Insertion Sort improves dramatically — from ~0.157s (random) to ~0.018s (nearly sorted) at n=3,000, roughly 8.5× faster. Because most elements are already close to their correct position, the inner while-loop runs very few iterations. This is Insertion Sort's adaptive behaviour: O(n·k) where k is the average displacement of each element.
Bubble Sort also improves somewhat — from ~0.327s (random) to ~0.204s (nearly sorted) at n=3,000, about 1.6× faster. It still scans the full array in every pass even when very few swaps are needed, which limits how much it benefits from partial order.
Merge Sort is essentially unchanged — ~0.004s in both experiments at n=3,000. It divides and merges every element regardless of input order, so partial sorting provides no benefit. Its O(n log n) runtime is consistent across all input types.

Key takeaway: For nearly sorted data, Insertion Sort is the standout — its adaptive nature makes it competitive with Merge Sort at moderate sizes. Bubble Sort gains some benefit but not nearly as much. Merge Sort is input-agnostic and remains reliably fast regardless of how sorted the data is.
