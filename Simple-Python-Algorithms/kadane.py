def kadane(arr):
    max_current = max_global = arr[0]

    for i in range(1, len(arr)):
        max_current = max(arr[i], max_current + arr[i])
        if max_current > max_global:
            max_global = max_current

    return max_global

# Get user input
arr = list(map(int, input("Enter numbers separated by spaces: ").split()))
print(f"The maximum subarray sum is: {kadane(arr)}")
