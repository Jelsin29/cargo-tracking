from typing import List, Any, Callable, Optional

def binary_search(arr: List[Any], target: Any, key: Callable = lambda x: x) -> Optional[int]:
    """
    Perform binary search on a sorted array.
    
    Args:
        arr: Sorted list of items
        target: Item to find
        key: Function to extract comparison key from items
    
    Returns:
        Index of found item or None if not found
    """
    if not arr:
        return None
        
    left, right = 0, len(arr) - 1
    
    while left <= right:
        mid = (left + right) // 2
        mid_val = key(arr[mid])
        
        if mid_val == target:
            return mid
        elif mid_val < target:
            left = mid + 1
        else:
            right = mid - 1
    
    return None

def linear_search(arr: List[Any], target: Any, key: Callable = lambda x: x) -> Optional[int]:
    """
    Perform linear search on an array.
    
    Args:
        arr: List of items
        target: Item to find
        key: Function to extract comparison key from items
    
    Returns:
        Index of found item or None if not found
    """
    for i, item in enumerate(arr):
        if key(item) == target:
            return i
    return None
