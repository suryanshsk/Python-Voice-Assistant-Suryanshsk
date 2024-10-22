def counting_sort(arr):
    max_val = max(arr)
    count = [0] * (max_val + 1)
    
    for num in arr:
        count[num] += 1
    
    index = 0
    for i in range(len(count)):
        while count[i] > 0:
            arr[index] = i
            index += 1
            count[i] -= 1

# Example usage:
arr = [4, 2, 2, 8, 3, 3, 1]
counting_sort(arr)
print("Counting Sorted Array:", arr)
