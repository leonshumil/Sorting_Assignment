# Sorting_Assignment

## Student Name
[Your Name Here]

## Selected Algorithms
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

The plot clearly shows the difference between O(n²) and O(n log n) algorithms on random input:

- **Bubble Sort** is the slowest. It takes ~3.6 seconds at n=10,000, and cannot be tested at larger sizes. Its runtime grows quadratically — doubling the size roughly quadruples the time.
- **Selection Sort** and **Insertion Sort** are also O(n²) and follow a similar quadratic curve. In practice, Selection Sort and Insertion Sort are about 2–3× faster than Bubble Sort because they perform fewer operations per pass, but they still cannot scale to large inputs.
- **Merge Sort** and **Quick Sort** are dramatically faster, following an O(n log n) growth curve. At n=1,000,000, Quick Sort finishes in ~1.76s and Merge Sort in ~2.81s, while the O(n²) algorithms cannot even reach that size. Quick Sort is consistently the fastest due to its in-place nature and excellent cache performance.

The shaded bands show one standard deviation across repetitions. Quick Sort and Merge Sort have very tight bands, indicating stable, predictable performance.

---

## Part C – Nearly Sorted Arrays (5% noise)

![result2](result2.png)

### Explanation – Did runtimes change vs. random input?

On nearly sorted arrays (only 5% of elements are randomly swapped), the runtimes changed noticeably for several algorithms:

- **Insertion Sort** improves dramatically — from ~1.44s to ~0.18s at n=10,000 (roughly **8× faster**). Because most elements are already close to their correct position, the inner loop runs very few iterations. This is Insertion Sort's best-case adaptive behaviour: O(n·k) where k is average displacement.
- **Bubble Sort** also improves somewhat (from ~3.6s to ~2.1s at n=10,000) but less than Insertion Sort, because it still scans the full array each pass regardless of how few swaps are needed.
- **Selection Sort** shows almost **no improvement** on nearly sorted data (~1.49s vs ~1.49s). This is because Selection Sort always scans the entire remaining unsorted portion to find the minimum, regardless of how sorted the array already is. It is non-adaptive by nature.
- **Merge Sort** and **Quick Sort** are essentially unchanged. Both algorithms process every element regardless of order, and their O(n log n) runtime is guaranteed for all input types. Quick Sort uses a median-of-three pivot, which prevents the O(n²) worst case that can occur on sorted input with naive pivot selection.

**Key takeaway:** For nearly sorted data, Insertion Sort is an excellent adaptive choice. Selection Sort is the most disappointing — it gains nothing from partial order. Merge Sort and Quick Sort remain consistently fast across all input types.
