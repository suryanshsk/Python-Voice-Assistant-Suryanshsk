def flood_fill(image, sr, sc, new_color):
    original_color = image[sr][sc]
    if original_color == new_color:
        return image

    def fill(r, c):
        if r < 0 or r >= len(image) or c < 0 or c >= len(image[0]):
            return
        if image[r][c] != original_color:
            return

        image[r][c] = new_color
        fill(r + 1, c)
        fill(r - 1, c)
        fill(r, c + 1)
        fill(r, c - 1)

    fill(sr, sc)
    return image

# Get user input
rows = int(input("Enter the number of rows in the image: "))
cols = int(input("Enter the number of columns in the image: "))
image = []
print("Enter the image row by row (space-separated values):")
for _ in range(rows):
    image.append(list(map(int, input().split())))

sr = int(input("Enter the starting row: "))
sc = int(input("Enter the starting column: "))
new_color = int(input("Enter the new color: "))

flood_fill(image, sr, sc, new_color)
print("Updated image after flood fill:")
for row in image:
    print(row)
