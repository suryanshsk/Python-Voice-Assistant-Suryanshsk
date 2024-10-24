def two_pointer(arr, target):
    left, right = 0, len(arr) - 1
    while left < right:
        current_sum = arr[left] + arr[right]
        if current_sum == target:
            return (arr[left], arr[right])
        elif current_sum < target:
            left += 1
        else:
            right -= 1
    return None

# Get user input
arr = list(map(int, input("Enter sorted numbers separated by spaces: ").split()))
target = int(input("Enter the target sum: "))
result = two_pointer(arr, target)

if result:
    print(f"The pair that sums to {target} is: {result}")
else:
    print("No pair found.")
