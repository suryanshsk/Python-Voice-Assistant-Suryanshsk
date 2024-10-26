def strand_sort(arr):
    if len(arr) <= 1:
        return arr

    result = []
    while arr:
        sublist = [arr.pop(0)]

        for i in range(len(arr)):
            if arr[i] > sublist[-1]:
                sublist.append(arr[i])
                arr.pop(i)

        result = merge(result, sublist)

    return result

def merge(left, right):
    result = []
    while left and right:
        if left[0] < right[0]:
            result.append(left.pop(0))
        else:
            result.append(right.pop(0))
    result.extend(left + right)
    return result

# Example usage:
arr = [10, 8, 1, 4, 6, 9]
arr = strand_sort(arr)
print("Strand Sorted Array:", arr)
