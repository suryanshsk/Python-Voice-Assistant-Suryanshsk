import math 
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import re
import plotly.graph_objs as go
import plotly.io as pio

def basic_arithmetic(op, a, b):
    try:
        if op == 'add':
            return a + b
        elif op == 'subtract':
            return a - b
        elif op == 'multiply':
            return a * b
        elif op == 'divide':
            return a / b if b != 0 else "Error: Cannot divide by zero"
        else:
            return "Error: Invalid operation"
    except Exception as e:
        return f"Error: {str(e)}"

def solve_equation(equation):
    try:
        x = sp.symbols('x')
        solution = sp.solve(equation, x)
        return solution
    except Exception as e:
        return f"Error solving equation: {str(e)}"


def trigonometric_function(func, angle):
    try:
        angle_rad = np.radians(angle)
        if func == 'sin':
            return np.sin(angle_rad)
        elif func == 'cos':
            return np.cos(angle_rad)
        elif func == 'tan':
            return np.tan(angle_rad)
        else:
            return "Error: Invalid trigonometric function"
    except Exception as e:
        return f"Error: {str(e)}"


def differentiate(expr):
    try:
        x = sp.symbols('x')
        return sp.diff(expr, x)
    except Exception as e:
        return f"Error in differentiation: {str(e)}"

def integrate(expr):
    try:
        x = sp.symbols('x')
        return sp.integrate(expr, x)
    except Exception as e:
        return f"Error in integration: {str(e)}"


def factorial(n):
    if n < 0:
        raise ValueError("Negative numbers do not have a factorial.")
    return math.factorial(n)


def fibonacci(n):
    try:
        if n <= 0:
            return "Error: Input must be a positive integer."
        seq = [0, 1]
        for i in range(2, n):
            seq.append(seq[-1] + seq[-2])
        return seq[:n]
    except Exception as e:
        return f"Error: {str(e)}"


def matrix_operations(matrix_a, matrix_b, operation):
    try:
        if operation == 'add':
            return np.add(matrix_a, matrix_b)
        elif operation == 'subtract':
            return np.subtract(matrix_a, matrix_b)
        elif operation == 'multiply':
            return np.dot(matrix_a, matrix_b)
        else:
            return "Error: Invalid matrix operation"
    except Exception as e:
        return f"Error: {str(e)}"

def plot_function(expr, x_range):
    try:
        x = sp.symbols('x')
        f = sp.lambdify(x, expr, 'numpy')

        x_vals = np.linspace(x_range[0], x_range[1], 1000)
        y_vals = f(x_vals)

        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=x_vals, y=y_vals,
            mode='lines',
            name=str(expr),
            line=dict(color='blue', width=2),
            hoverinfo='x+y',  
        ))

        fig.add_trace(go.Scatter(
            x=[x_range[0], x_range[1]], y=[0, 0],
            mode='lines',
            line=dict(color='black', dash='dash'),
            hoverinfo='skip',
            showlegend=False
        ))
        fig.add_trace(go.Scatter(
            x=[0, 0], y=[min(y_vals), max(y_vals)],
            mode='lines',
            line=dict(color='black', dash='dash'),
            hoverinfo='skip',
            showlegend=False
        ))
        fig.update_layout(
            title=f'Plot of {str(expr)}',
            xaxis_title='x',
            yaxis_title='f(x)',
            xaxis=dict(
                zeroline=True,
                showline=True,
                showgrid=True,
                gridcolor='lightgray',
                zerolinecolor='black'
            ),
            yaxis=dict(
                zeroline=True,
                showline=True,
                showgrid=True,
                gridcolor='lightgray',
                zerolinecolor='black'
            ),
            plot_bgcolor='white', 
            hovermode="closest",   
        )

        fig.show()

    except Exception as e:
        return f"Error in plotting: {str(e)}"

def statistical_analysis(data):
    try:
        mean = np.mean(data)
        median = np.median(data)
        std_dev = np.std(data)
        variance = np.var(data)
        correlation = np.corrcoef(data) if len(data) > 1 else None
        regression = stats.linregress(range(len(data)), data) if len(data) > 1 else None
        
        return {
            'mean': mean,
            'median': median,
            'std_dev': std_dev,
            'variance': variance,
            'correlation': correlation[0, 1] if correlation is not None and correlation.shape == (2, 2) else None,
            'slope': regression.slope if regression else None,
            'intercept': regression.intercept if regression else None
        }
    except Exception as e:
        return f"Error in statistical analysis: {str(e)}"


def complex_operations(op, a, b):
    try:
        a_complex = complex(a)
        b_complex = complex(b)
        
        if op == 'add':
            return a_complex + b_complex
        elif op == 'subtract':
            return a_complex - b_complex
        elif op == 'multiply':
            return a_complex * b_complex
        elif op == 'divide':
            return a_complex / b_complex if b_complex != 0 else "Error: Cannot divide by zero"
        else:
            return "Error: Invalid operation"
    except Exception as e:
        return f"Error: {str(e)}"


def unit_conversion(value, from_unit, to_unit):
    conversion_factors = {
        'meters_to_feet': 3.28084,
        'feet_to_meters': 1 / 3.28084,
        'kilograms_to_pounds': 2.20462,
        'pounds_to_kilograms': 1 / 2.20462,
        # Add more conversions as needed
    }
    
    try:
        key = f"{from_unit}_to_{to_unit}"
        if key in conversion_factors:
            return value * conversion_factors[key]
        else:
            return "Error: Conversion not supported."
    except Exception as e:
        return f"Error: {str(e)}"

# Extraction functions
def extract_numbers(command):
    numbers = list(map(float, re.findall(r'-?\d+\.?\d*', command)))
    return numbers

def extract_equation(command):
    # Extract equation like "x**2 - 4"
    equation = re.search(r'solve (.+)', command)
    return sp.sympify(equation.group(1)) if equation else None

def extract_expression(command):
    # Extract expression for differentiation or integration
    expression = re.search(r'differentiate (.+)|integrate (.+)', command)
    return sp.sympify(expression.group(1) or expression.group(2)) if expression else None

def extract_trig_function(command):
    if "sin" in command:
        return "sin"
    elif "cos" in command:
        return "cos"
    elif "tan" in command:
        return "tan"
    return None

def extract_angle(command):
    angle = re.search(r'(\d+)', command)
    return float(angle.group(1)) if angle else None

def extract_matrix_a(command):
    # Example: extract matrix A from "matrix A is [[1, 2], [3, 4]]"
    matrix_a = re.search(r'matrix A is (\[\[.*?\]\])', command)
    return np.array(eval(matrix_a.group(1))) if matrix_a else None

def extract_matrix_b(command):
    # Example: extract matrix B from "matrix B is [[5, 6], [7, 8]]"
    matrix_b = re.search(r'matrix B is (\[\[.*?\]\])', command)
    return np.array(eval(matrix_b.group(1))) if matrix_b else None

def extract_matrix_operation(command):
    if "add" in command:
        return 'add'
    elif "subtract" in command:
        return 'subtract'
    elif "multiply" in command:
        return 'multiply'
    return None

def extract_complex_numbers(command):
    # Example: extract complex numbers from "complex 1+2j and 3+4j"
    numbers = re.findall(r'[-+]?\d*\.?\d*[-+]\d*\.?\d*j', command)
    return [n.strip() for n in numbers] if numbers else [None, None]

def extract_complex_operation(command):
    if "add" in command:
        return 'add'
    elif "subtract" in command:
        return 'subtract'
    elif "multiply" in command:
        return 'multiply'
    elif "divide" in command:
        return 'divide'
    return None

def extract_units(command):
    # Example: extract value and units from "convert 10 meters to feet"
    match = re.search(r'convert (\d+\.?\d*) (\w+) to (\w+)', command)
    if match:
        value = float(match.group(1))
        from_unit = match.group(2)
        to_unit = match.group(3)
        return value, from_unit, to_unit
    return None, None, None

def extract_range(command):
    # Example: extract range from "plot x**2 from -10 to 10"
    match = re.search(r'plot (.+) from (-?\d+) to (-?\d+)', command)
    if match:
        expr = sp.sympify(match.group(1))
        x_range = (float(match.group(2)), float(match.group(3)))
        return expr, x_range
    return None, None


def process_command(command):
    try:
        if "solve" in command:
            equation = extract_equation(command)
            return solve_equation(equation)
        
        elif "add" in command or "subtract" in command or "multiply" in command or "divide" in command:
            numbers = extract_numbers(command)
            op = 'add' if 'add' in command else 'subtract' if 'subtract' in command else 'multiply' if 'multiply' in command else 'divide'
            return basic_arithmetic(op, numbers[0], numbers[1])
        
        elif "factorial" in command:
            n = int(extract_numbers(command)[0])  
            return factorial(n)
        
        elif "fibonacci" in command:
            n = int(extract_numbers(command)[0])  
            return fibonacci(n)
        
        elif "differentiate" in command or "integrate" in command:
            expression = extract_expression(command)
            return differentiate(expression) if "differentiate" in command else integrate(expression)
        
        elif "sin" in command or "cos" in command or "tan" in command:
            func = extract_trig_function(command)
            angle = extract_angle(command)
            return trigonometric_function(func, angle)
        
        elif "matrix" in command:
            matrix_a = extract_matrix_a(command)
            matrix_b = extract_matrix_b(command)
            operation = extract_matrix_operation(command)
            return matrix_operations(matrix_a, matrix_b, operation)
        
        elif "complex" in command:
            operation = extract_complex_operation(command)
            numbers = extract_complex_numbers(command)
            return complex_operations(operation, numbers[0], numbers[1])
        
        elif "convert" in command:
            value, from_unit, to_unit = extract_units(command)
            return unit_conversion(value, from_unit, to_unit)
        
        elif "plot" in command:
            expr, x_range = extract_range(command)
            return plot_function(expr, x_range)
        
        elif "statistical" in command:
            data = extract_numbers(command)
            return statistical_analysis(data)
        
        else:
            return "Error: Command not recognized."
        
    except Exception as e:
        return f"Error processing command: {str(e)}"


if __name__ == "__main__":
    print("Testing Phase-")  
    print(basic_arithmetic('add', 10, 5))  # Output: 15
    print(solve_equation(sp.sympify('x**2 - 4')))  # Output: [-2, 2]
    print(trigonometric_function('sin', 30))  # Output: 0.5
    print(differentiate(sp.sympify('x**3 + x')))  # Output: 3*x**2 + 1
    print(integrate(sp.sympify('x**2')))  # Output: x**3/3
    print(factorial(5))  # Output: 120
    print(fibonacci(10))  # Output: [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]

    # Example commands for testing
    print(process_command("solve x**2 - 4"))  # Output: [-2, 2]
    print(process_command("add 10 and 5"))  # Output: 15
    print(process_command("differentiate x**3 + x"))  # Output: 3*x**2 + 1
    print(process_command("statistical analysis [1, 2, 3, 4, 5]"))  # Output: {'mean': 3.0, 'median': 3.0, 'std_dev': 1.4142135623730951, 'variance': 2.0, 'correlation': None, 'slope': 1.0, 'intercept': 1.0}
    print(process_command("plot x**3 from -10 to 10"))  # Generates a plot
    print(process_command("convert 10 meters to feet"))  # Output: 32.8084

def user_input():
    while True: 
        print("\nWelcome to the Maths Solver!")
        print("Choose the operation you want to perform:")
        print("1. Basic Arithmetic (add, subtract, multiply, divide)")
        print("2. Solve Equation")
        print("3. Trigonometric Function (sin, cos, tan)")
        print("4. Differentiation")
        print("5. Integration")
        print("6. Factorial")
        print("7. Fibonacci")
        print("8. Matrix Operations (add, subtract, multiply)")
        print("9. Complex Number Operations (add, subtract, multiply, divide)")
        print("10. Unit Conversion")
        print("11. Plot Function")
        print("12. Statistical Analysis")
        print("13. Exit")  
        
        choice = input("Enter the number of your choice: ")

        if choice == '1':
            a = float(input("Enter first number: "))
            b = float(input("Enter second number: "))
            operation = input("Enter operation (add, subtract, multiply, divide): ").lower()
            print(f"Result: {basic_arithmetic(operation, a, b)}")

        elif choice == '2':
            equation = input("Enter the equation to solve (e.g., x**2 - 4): ")
            x = sp.symbols('x')
            equation_expr = sp.sympify(equation)
            print(f"Solution: {solve_equation(equation_expr)}")

        elif choice == '3':
            angle = float(input("Enter the angle (in degrees): "))
            function = input("Enter the trigonometric function (sin, cos, tan): ").lower()
            print(f"Result: {trigonometric_function(function, angle)}")

        elif choice == '4':
            expression = input("Enter the expression to differentiate (e.g., x**3 + x): ")
            expr = sp.sympify(expression)
            print(f"Derivative: {differentiate(expr)}")

        elif choice == '5':
            expression = input("Enter the expression to integrate (e.g., x**2): ")
            expr = sp.sympify(expression)
            print(f"Integral: {integrate(expr)}")

        elif choice == '6':
            n = int(input("Enter a number for factorial: "))
            print(f"Factorial: {factorial(n)}")

        elif choice == '7':
            n = int(input("Enter the number of Fibonacci terms to generate: "))
            print(f"Fibonacci sequence: {fibonacci(n)}")

        elif choice == '8':
            matrix_a = eval(input("Enter matrix A (e.g., [[1, 2], [3, 4]]): "))
            matrix_b = eval(input("Enter matrix B (e.g., [[5, 6], [7, 8]]): "))
            operation = input("Enter matrix operation (add, subtract, multiply): ").lower()
            print(f"Matrix Result: {matrix_operations(np.array(matrix_a), np.array(matrix_b), operation)}")

        elif choice == '9':
            a = input("Enter the first complex number (e.g., 1+2j): ")
            b = input("Enter the second complex number (e.g., 3+4j): ")
            operation = input("Enter complex operation (add, subtract, multiply, divide): ").lower()
            print(f"Result: {complex_operations(operation, a, b)}")

        elif choice == '10':
            value = float(input("Enter the value to convert: "))
            from_unit = input("Enter the from unit (e.g., meters, kilograms): ").lower()
            to_unit = input("Enter the to unit (e.g., feet, pounds): ").lower()
            print(f"Converted Value: {unit_conversion(value, from_unit, to_unit)}")

        elif choice == '11':
            expression = input("Enter the function to plot (e.g., x**3): ")
            x_range = eval(input("Enter the x-range as a tuple (e.g., (-10, 10)): "))
            expr = sp.sympify(expression)
            plot_function(expr, x_range)

        elif choice == '12':
            data = eval(input("Enter the data for statistical analysis (e.g., [1, 2, 3, 4, 5]): "))
            print(f"Statistical Analysis: {statistical_analysis(data)}")

        elif choice == '13':
            print("Exiting the Maths Solver. Goodbye!")
            break 

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    user_input() 
