def bucket_sort(arr):
    bucket = [[] for _ in range(len(arr))]
    for num in arr:
        index = int(len(arr) * num)
        bucket[index].append(num)
    
    for i in range(len(arr)):
        bucket[i] = sorted(bucket[i])

    k = 0
    for i in range(len(arr)):
        for j in range(len(bucket[i])):
            arr[k] = bucket[i][j]
            k += 1

# Example usage:
arr = [0.78, 0.17, 0.39, 0.72, 0.94, 0.18, 0.12, 0.64]
bucket_sort(arr)
print("Bucket Sorted Array:", arr)
