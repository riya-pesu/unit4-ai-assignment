import pytest
from bubble_sort import bubble_sort, bubble_sort_in_place

def test_bubble_sort_basic():
    assert bubble_sort([3, 1, 2]) == [1, 2, 3]

def test_bubble_sort_reverse():
    assert bubble_sort([1, 2, 3], reverse=True) == [3, 2, 1]

def test_in_place_mutation():
    lst = [4, 2, 1]
    res = bubble_sort(lst, in_place=True)
    assert res is lst
    assert lst == [1, 2, 4]

def test_in_place_requires_list():
    with pytest.raises(TypeError):
        bubble_sort((3, 1), in_place=True)  # tuple is not allowed for in-place

def test_non_iterable_raises():
    with pytest.raises(TypeError):
        bubble_sort(123)  # int is not iterable

def test_comparison_type_error():
    # Mixing incomparable types should raise a TypeError from comparisons
    with pytest.raises(TypeError):
        bubble_sort([1, "a"])
