def gnome_sort(arr):
    index = 0
    while index < len(arr):
        if index == 0 or arr[index] >= arr[index - 1]:
            index += 1
        else:
            arr[index], arr[index - 1] = arr[index - 1], arr[index]
            index -= 1

# Example usage:
arr = [34, 2, 10, -9]
gnome_sort(arr)
print("Gnome Sorted Array:", arr)
