class Node:
    def __init__(self, key):
        self.left = None
        self.right = None
        self.val = key

def insert(root, key):
    if root is None:
        return Node(key)
    else:
        if key < root.val:
            root.left = insert(root.left, key)
        else:
            root.right = insert(root.right, key)
    return root

def inorder_traversal(root, result):
    if root:
        inorder_traversal(root.left, result)
        result.append(root.val)
        inorder_traversal(root.right, result)

def tree_sort(arr):
    if len(arr) == 0:
        return []
    
    root = None
    for key in arr:
        root = insert(root, key)

    result = []
    inorder_traversal(root, result)
    return result

# Example usage:
arr = [5, 4, 7, 2, 11]
arr = tree_sort(arr)
print("Tree Sorted Array:", arr)
