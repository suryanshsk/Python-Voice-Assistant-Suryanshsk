def bitonic_merge(arr, low, cnt, direction):
    if cnt > 1:
        k = cnt // 2
        for i in range(low, low + k):
            if (direction == 1 and arr[i] > arr[i + k]) or (direction == 0 and arr[i] < arr[i + k]):
                arr[i], arr[i + k] = arr[i + k], arr[i]
        bitonic_merge(arr, low, k, direction)
        bitonic_merge(arr, low + k, k, direction)

def bitonic_sort(arr, low, cnt, direction):
    if cnt > 1:
        k = cnt // 2
        bitonic_sort(arr, low, k, 1)  # ascending
        bitonic_sort(arr, low + k, k, 0)  # descending
        bitonic_merge(arr, low, cnt, direction)

def sort_bitonic(arr):
    bitonic_sort(arr, 0, len(arr), 1)

# Example usage:
arr = [19, 2, 5, 11, 6, 3, 7]
sort_bitonic(arr)
print("Bitonic Sorted Array:", arr)
