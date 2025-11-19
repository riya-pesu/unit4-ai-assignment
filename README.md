# 🧮 Bubble Sort — unit4-ai-assignment

This repository contains a simple, well-documented implementation of the Bubble Sort
algorithm in Python.

Features
- Clear docstrings and examples
- Input validation and helpful error messages
- Command-line interface for quick experiments

## 🚀 Steps to Run the Program

Clone the repository:

```bash
git clone https://github.com/riya-pesu/unit4-ai-assignment.git
cd unit4-ai-assignment
```

Run the sorter with positional items (integers/floats are detected automatically):

```bash
# Sort ascending
python3 bubble_sort.py 5 1 4 3 2

# Sort descending
python3 bubble_sort.py --reverse 5 1 4 3 2

# Verbose output (shows original and sorted)
python3 bubble_sort.py -v 3 2 1
```

Run interactively (enter a comma-separated list when prompted):

```bash
python3 bubble_sort.py
# Enter items separated by commas (e.g. 3, 1, 2 or a, b, c)
```

## 📋 Examples

- Sorting numbers:
  - `python3 bubble_sort.py 10 4 7 1 9` → `1 4 7 9 10`

- Sorting strings:
  - `python3 bubble_sort.py apple banana cherry` → `apple banana cherry`

## 🛠️ Requirements

- Python 3.8+ (should work on 3.7 as well, but 3.8+ recommended)

## ❗ Notes

- The bubble sort implementation is educational (O(n^2)). For large lists, prefer
  Python's built-in `sorted()` for performance.
- If elements in the list cannot be compared with each other (e.g., trying to
  compare a dict with an int), the program will raise a helpful TypeError showing
  which elements couldn't be compared.

Happy sorting! 🎉
