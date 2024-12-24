import time
from typing import List, Any, Callable

def merge_sort(arr: List[Any], key: Callable = lambda x: x) -> List[Any]:
    """
    Sort array using merge sort algorithm.
    
    Args:
        arr: List to sort
        key: Function to extract comparison key from items
    
    Returns:
        Sorted list
    """
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left = merge_sort(arr[:mid], key)
    right = merge_sort(arr[mid:], key)
    
    return merge(left, right, key)

def merge(left: List[Any], right: List[Any], key: Callable) -> List[Any]:
    """
    Merge two sorted arrays.
    
    Args:
        left: First sorted array
        right: Second sorted array
        key: Function to extract comparison key from items
    
    Returns:
        Merged sorted array
    """
    result = []
    i = j = 0
    
    while i < len(left) and j < len(right):
        if key(left[i]) <= key(right[j]):
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    
    result.extend(left[i:])
    result.extend(right[j:])
    return result

def quick_sort(arr: List[Any], key: Callable = lambda x: x) -> List[Any]:
    """
    Sort array using quicksort algorithm.
    
    Args:
        arr: List to sort
        key: Function to extract comparison key from items
    
    Returns:
        Sorted list
    """
    if len(arr) <= 1:
        return arr
    
    def partition(low: int, high: int) -> int:
        pivot = arr[high]
        i = low - 1
        
        for j in range(low, high):
            if key(arr[j]) <= key(pivot):
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
        
        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        return i + 1

    def quick_sort_helper(low: int, high: int):
        if low < high:
            pi = partition(low, high)
            quick_sort_helper(low, pi - 1)
            quick_sort_helper(pi + 1, high)
    
    # Create a copy of the array to avoid modifying the original
    arr_copy = arr.copy()
    quick_sort_helper(0, len(arr_copy) - 1)
    return arr_copy

def measure_sorting_time(func: Callable, arr: List[Any], key: Callable = lambda x: x) -> float:
    """
    Measure the execution time of a sorting function.
    
    Args:
        func: Sorting function to measure
        arr: Array to sort
        key: Key function for sorting
    
    Returns:
        Execution time in seconds
    """
    start_time = time.time()
    func(arr.copy(), key)  # Use a copy to avoid modifying original array
    end_time = time.time()
    return end_time - start_time