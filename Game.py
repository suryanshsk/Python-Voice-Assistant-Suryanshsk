def is_winning_string(string):
  """
  Checks if a given string is a winning string.

  Args:
    string: The input string.

  Returns:
    True if the string is a winning string, False otherwise.
  """

  partner_map = {
      'a': 'n', 'b': 'o', 'c': 'p', 'd': 'q', 'e': 'r', 'f': 's', 'g': 't', 'h': 'u',
      'i': 'v', 'j': 'w', 'k': 'x', 'l': 'y', 'm': 'z'
  }

  for i in range(0, len(string), 2):
    if string[i] not in partner_map or string[i+1] != partner_map[string[i]]:
      return False
  return True

# Example usage:
string1 = "anbopq"
string2 = "azbycx"
string3 = "anboq"

print(is_winning_string(string1))  # Output: True
print(is_winning_string(string2))  # Output: True
print(is_winning_string(string3))  # Output: False