def max_sum_subarray(arr, k):
    max_sum = sum(arr[:k])
    window_sum = max_sum

    for i in range(len(arr) - k):
        window_sum = window_sum - arr[i] + arr[i + k]
        max_sum = max(max_sum, window_sum)

    return max_sum

# Get user input
arr = list(map(int, input("Enter numbers separated by spaces: ").split()))
k = int(input("Enter the size of the subarray: "))
print(f"The maximum sum of a subarray of size {k} is: {max_sum_subarray(arr, k)}")
