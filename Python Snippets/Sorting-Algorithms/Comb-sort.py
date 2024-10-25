def comb_sort(arr):
    gap = len(arr)
    shrink = 1.3
    sorted = False

    while not sorted:
        gap = int(gap / shrink)
        if gap <= 1:
            gap = 1
            sorted = True
        
        for i in range(len(arr) - gap):
            if arr[i] > arr[i + gap]:
                arr[i], arr[i + gap] = arr[i + gap], arr[i]
                sorted = False

# Example usage:
arr = [8, 4, 1, 56, 3, -44, 23, -6, 28, 0]
comb_sort(arr)
print("Comb Sorted Array:", arr)
