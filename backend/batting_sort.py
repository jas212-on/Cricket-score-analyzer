"""
Heap Sort Implementation for Cricket Batting Statistics
Sorts batters by runs, strike rate, fours, and sixes
"""

def heapify(arr, n, i, key):
    """
    Heapify subtree rooted at index i
    n = size of heap
    key = lambda function to extract sort key
    """
    largest = i
    left = 2 * i + 1
    right = 2 * i + 2
    
    # Check if left child exists and is greater
    if left < n and key(arr[left]) > key(arr[largest]):
        largest = left
    
    # Check if right child exists and is greater
    if right < n and key(arr[right]) > key(arr[largest]):
        largest = right
    
    # If largest is not root, swap and continue heapifying
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        heapify(arr, n, largest, key)


def heap_sort(arr, key):
    """
    Perform heap sort on array based on key function
    Returns sorted array in descending order
    """
    if not arr:
        return arr
    
    n = len(arr)
    
    # Build max heap
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i, key)
    
    # Extract elements from heap one by one
    for i in range(n - 1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]  # Swap
        heapify(arr, i, 0, key)
    
    # Reverse to get descending order
    arr.reverse()
    return arr


def sort_batting_stats(batter_list):
    """
    Sort batting statistics using heap sort
    
    Input: List of dicts with keys: player, runs, balls, sr, fours, sixes
    Output: Dict with four sorted lists
    """
    # Create copies for different sorts
    import copy
    
    sorted_by_runs = copy.deepcopy(batter_list)
    sorted_by_sr = copy.deepcopy(batter_list)
    sorted_by_fours = copy.deepcopy(batter_list)
    sorted_by_sixes = copy.deepcopy(batter_list)
    
    # Sort by runs (descending)
    heap_sort(sorted_by_runs, key=lambda x: x["runs"])
    
    # Sort by strike rate (descending)
    heap_sort(sorted_by_sr, key=lambda x: x["sr"])
    
    # Sort by fours (descending)
    heap_sort(sorted_by_fours, key=lambda x: x["fours"])
    
    # Sort by sixes (descending)
    heap_sort(sorted_by_sixes, key=lambda x: x["sixes"])
    
    return {
        "sorted_by_runs": sorted_by_runs,
        "sorted_by_sr": sorted_by_sr,
        "sorted_by_fours": sorted_by_fours,
        "sorted_by_sixes": sorted_by_sixes
    }


# Test with sample data
if __name__ == "__main__":
    sample_batters = [
        {"player": "Player A", "runs": 45, "balls": 30, "sr": 150.0, "fours": 4, "sixes": 2},
        {"player": "Player B", "runs": 78, "balls": 50, "sr": 156.0, "fours": 8, "sixes": 3},
        {"player": "Player C", "runs": 23, "balls": 20, "sr": 115.0, "fours": 2, "sixes": 1},
    ]
    
    result = sort_batting_stats(sample_batters)
    
    print("Sorted by Runs:")
    for b in result["sorted_by_runs"]:
        print(f"  {b['player']}: {b['runs']} runs")
    
    print("\nSorted by Strike Rate:")
    for b in result["sorted_by_sr"]:
        print(f"  {b['player']}: {b['sr']} SR")
    
    print("\nSorted by Fours:")
    for b in result["sorted_by_fours"]:
        print(f"  {b['player']}: {b['fours']} fours")
    
    print("\nSorted by Sixes:")
    for b in result["sorted_by_sixes"]:
        print(f"  {b['player']}: {b['sixes']} sixes")