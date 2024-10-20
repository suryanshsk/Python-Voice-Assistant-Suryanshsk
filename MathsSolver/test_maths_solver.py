import unittest
from MathsSolver.maths_solver import process_command, factorial, differentiate, integrate, fibonacci  # Adjust the import based on your module name

class TestMathsSolver(unittest.TestCase):
    
    def test_factorial(self):
        self.assertEqual(factorial(5), 120)
        self.assertRaises(ValueError, factorial, -1)

    def test_fibonacci(self):
        self.assertEqual(fibonacci(5), [0, 1, 1, 2, 3])
        self.assertEqual(fibonacci(0), "Error: Input must be a positive integer.")

    def test_differentiate(self):
        self.assertEqual(str(differentiate('x**3 + x')), '3*x**2 + 1')

    def test_integrate(self):
        self.assertEqual(str(integrate('x**2')), 'x**3/3')

    def test_process_command(self):
        self.assertEqual(process_command("factorial 5"), 120)
        self.assertEqual(process_command("fibonacci 5"), [0, 1, 1, 2, 3])
        self.assertEqual(str(process_command("differentiate x**3 + x")), '3*x**2 + 1')
        self.assertEqual(str(process_command("integrate x**2")), 'x**3/3')
        self.assertEqual(process_command("add 10 and 5"), 15)

if __name__ == '__main__':
    unittest.main()
