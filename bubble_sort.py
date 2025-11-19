#!/usr/bin/env python3
"""
bubble_sort.py

A small, well-documented implementation of the Bubble Sort algorithm with
input validation and helpful error messages.

Features
- bubble_sort(sequence, reverse=False, in_place=False): stable bubble sort
  implementation that either returns a new sorted list or sorts a provided list
  in place.
- Command-line interface to sort items provided as arguments or via prompt.
- Tries to interpret numeric inputs (int/float) automatically; leaves other
  items as strings so they can still be sorted lexicographically.
- Robust error handling for non-iterable inputs and non-comparable elements.

Complexity
- Time: O(n^2) worst-case
- Space: O(1) additional (when in_place=True) or O(n) for the returned copy

Author: GitHub Copilot (riya-pesu request)
"""

from typing import Iterable, List, Any
import argparse
import sys

__all__ = ["bubble_sort"]


def bubble_sort(sequence: Iterable[Any], *, reverse: bool = False, in_place: bool = False) -> List[Any]:
    """
    Sorts a sequence using the bubble sort algorithm.

    Parameters
    - sequence: An iterable of comparable items (numbers, strings, or any objects
      that implement comparison operators).
    - reverse: If True, sort in descending order. Default is False (ascending).
    - in_place: If True, attempt to sort the provided list object in place.
      - Must be passed a list object (not a tuple or generator).
      - If in_place=True and sequence is not a list, a TypeError is raised.
      - Default is False: the function returns a new sorted list and does not
        mutate the input.

    Returns
    - A list containing the sorted items. If in_place=True and sequence is a list,
      the same list object is returned after being mutated.

    Raises
    - TypeError: If `sequence` is not iterable.
    - TypeError: If in_place=True but `sequence` is not a list.
    - TypeError: If two elements are found that cannot be compared with each other.
      The exception message will include the indices and the values that failed
      to compare.

    Examples
    >>> bubble_sort([3, 1, 2])
    [1, 2, 3]
    >>> bubble_sort(["c", "a", "b"], reverse=True)
    ['c', 'b', 'a']
    >>> lst = [4, 2, 1]
    >>> bubble_sort(lst, in_place=True) is lst
    True
    """
    # Validate iterability
    if not hasattr(sequence, "__iter__"):
        raise TypeError("The 'sequence' argument must be iterable (e.g., list, tuple).")

    # Handle in_place parameter
    if in_place:
        if not isinstance(sequence, list):
            raise TypeError("in_place=True requires a list object (mutable).")
        arr = sequence
    else:
        # Make a shallow copy so we do not mutate the caller's sequence
        arr = list(sequence)

    n = len(arr)
    if n < 2:
        # Nothing to sort
        return arr

    # Perform bubble sort
    # We use XOR-style comparison to reuse same logic for reverse parameter:
    # swap when (arr[j] > arr[j+1]) is True for ascending,
    # or when False for descending (hence XOR with reverse flag).
    for i in range(n):
        swapped = False
        # Last i elements are already in place
        for j in range(0, n - i - 1):
            try:
                should_swap = (arr[j] > arr[j + 1]) ^ reverse
            except TypeError as exc:
                # Provide a clear error showing where the comparison failed
                raise TypeError(
                    f"Cannot compare elements at positions {j} and {j+1}: {arr[j]!r} vs {arr[j+1]!r}"
                ) from exc

            if should_swap:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True

        if not swapped:
            # List is sorted early
            break

    return arr


def _parse_item(token: str) -> Any:
    """
    Try to parse a token into int or float. If both conversions fail, return the
    original string (stripped).

    This helps the CLI accept numeric inputs naturally while still supporting
    string sorting.
    """
    s = token.strip()
    # Try int
    try:
        return int(s)
    except ValueError:
        pass
    # Try float
    try:
        return float(s)
    except ValueError:
        pass
    # Fallback to string
    return s


def _cli(argv: List[str]) -> int:
    parser = argparse.ArgumentParser(
        prog="bubble_sort.py",
        description="Simple bubble sort implementation (educational)."
    )
    parser.add_argument(
        "items",
        nargs="*",
        help="Items to sort. If omitted, you will be prompted to enter a comma-separated list."
    )
    parser.add_argument(
        "-r", "--reverse",
        action="store_true",
        help="Sort in descending order."
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Show the result and a short summary."
    )

    args = parser.parse_args(argv)

    if not args.items:
        try:
            raw = input("Enter items separated by commas (e.g. 3, 1, 2 or a, b, c): ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nNo input provided. Exiting.", file=sys.stderr)
            return 1
        if not raw:
            print("No items entered. Exiting.", file=sys.stderr)
            return 1
        tokens = [t for t in raw.split(",")]
    else:
        tokens = args.items

    items = [_parse_item(t) for t in tokens]

    try:
        sorted_items = bubble_sort(items, reverse=args.reverse, in_place=False)
    except TypeError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2

    if args.verbose:
        print("Original:", items)
        print("Sorted:  ", sorted_items)
    else:
        # Print a simple one-line representation
        print(" ".join(map(str, sorted_items)))

    return 0


if __name__ == "__main__":
    raise SystemExit(_cli(sys.argv[1:]))
