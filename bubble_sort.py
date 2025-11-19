#!/usr/bin/env python3
"""
bubble_sort.py

Concise, readable bubble sort with minimal surface area:
- bubble_sort(sequence, reverse=False, in_place=False)
- bubble_sort_in_place(list, reverse=False)
- small CLI for quick use

This refactor adds explicit docstrings to the previously compact functions
so each part of the module is documented for maintainers and automated tools.

Preserves helpful TypeError messages for non-iterable inputs and
non-comparable elements while keeping the implementation compact.
"""
from typing import Iterable, List, Any
import argparse
import sys

__all__ = ["bubble_sort", "bubble_sort_in_place"]


def _parse_token(tok: str) -> Any:
    """
    Convert a CLI token to int or float when possible, otherwise return
    the stripped string.

    This helper keeps the CLI friendly to numeric inputs while preserving
    lexicographic sorting for non-numeric tokens.

    Args:
        tok: Raw token string from CLI or interactive input.

    Returns:
        int | float | str: Parsed value.
    """
    t = tok.strip()
    for conv in (int, float):
        try:
            return conv(t)
        except Exception:
            continue
    return t


def bubble_sort_in_place(arr: List[Any], *, reverse: bool = False) -> List[Any]:
    """
    Sort a list in place using the bubble sort algorithm.

    The algorithm is stable and has O(n^2) worst-case time complexity. This
    function mutates the provided list and also returns it for convenience.

    Args:
        arr: A list of comparable items to sort.
        reverse: If True, sort in descending order (largest first).

    Returns:
        The same list instance after being sorted.

    Raises:
        TypeError: If arr is not a list or if two elements cannot be compared.
    """
    if not isinstance(arr, list):
        raise TypeError("bubble_sort_in_place requires a list for in-place sorting.")
    n = len(arr)
    for end in range(n - 1, 0, -1):
        swapped = False
        for i in range(end):
            try:
                if (arr[i] > arr[i + 1]) ^ reverse:
                    arr[i], arr[i + 1] = arr[i + 1], arr[i]
                    swapped = True
            except TypeError as exc:
                raise TypeError(f"Cannot compare {arr[i]!r} and {arr[i+1]!r}") from exc
        if not swapped:
            break
    return arr


def bubble_sort(sequence: Iterable[Any], *, reverse: bool = False, in_place: bool = False) -> List[Any]:
    """
    Sort an iterable using bubble sort.

    This wrapper accepts any iterable; when in_place is True it requires
    a list and will sort it directly. When in_place is False (default), a new
    list copy is created and sorted, leaving the original iterable untouched.

    Args:
        sequence: Iterable of comparable items.
        reverse: If True, sort in descending order.
        in_place: If True, attempt to sort the given object in place (must be a list).

    Returns:
        A list with the sorted items (same instance if in_place=True and input was a list).

    Raises:
        TypeError: If sequence is not iterable, or if in_place=True and sequence is not a list.
    """
    if not hasattr(sequence, "__iter__"):
        raise TypeError("sequence must be iterable")
    if in_place:
        # caller asserts it's a list for in-place sorting; bubble_sort_in_place will validate
        return bubble_sort_in_place(sequence, reverse=reverse)  # type: ignore[arg-type]
    return bubble_sort_in_place(list(sequence), reverse=reverse)


def _cli(argv: List[str]) -> int:
    """
    Minimal command-line interface.

    Accepts positional items or prompts interactively (comma-separated).
    Returns:
        Exit code (0 success, 1 user/input error, 2 comparison error).
    """
    p = argparse.ArgumentParser(description="Bubble sort (concise).")
    p.add_argument("items", nargs="*", help="Items to sort (space separated).")
    p.add_argument("-r", "--reverse", action="store_true", help="Sort descending.")
    p.add_argument("-v", "--verbose", action="store_true", help="Show original + sorted.")
    args = p.parse_args(argv)

    if not args.items:
        try:
            raw = input("Enter items (comma separated): ").strip()
        except (EOFError, KeyboardInterrupt):
            return 1
        if not raw:
            return 1
        tokens = [t for t in raw.split(",")]
    else:
        tokens = args.items

    items = [_parse_token(t) for t in tokens]
    try:
        out = bubble_sort(items, reverse=args.reverse, in_place=False)
    except TypeError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2

    if args.verbose:
        print("Original:", items)
        print("Sorted:  ", out)
    else:
        print(" ".join(map(str, out)))
    return 0


if __name__ == "__main__":
    raise SystemExit(_cli(sys.argv[1:]))
