def parse_input(equation):
    """Parse input string (e.g., 'TWO+TWO=FOUR') to extract operands and result."""
    # Remove any extra whitespace
    equation = equation.replace(" ", "")
    
    # Check if equation contains '='
    if '=' not in equation:
        raise ValueError("Input must contain '='")
    
    # Split equation into left side (operands) and right side (result)
    parts = equation.split('=')
    if len(parts) != 2:
        raise ValueError("Input must have exactly one '='")
    left_side, right = parts
    
    # Check if left side contains '+'
    if '+' not in left_side:
        raise ValueError("Input must contain '+' in the left side")
    
    # Split left side into two operands
    operand_parts = left_side.split('+')
    if len(operand_parts) != 2:
        raise ValueError("Left side must have exactly two operands separated by '+'")
    operand1, operand2 = operand_parts
    
    # Validate that operands and result are non-empty and contain only uppercase letters
    if not (operand1.isupper() and operand2.isupper() and right.isupper()):
        raise ValueError("Operands and result must contain only uppercase letters")
    
    # Get unique letters in alphabetical order
    letters = sorted(set(operand1 + operand2 + right))
    # Identify leading letters (cannot be 0)
    leading_letters = {operand1[0], operand2[0], right[0]}
    return operand1, operand2, right, letters, leading_letters

def check_addition(assignment, operand1, operand2, result):
    """Check if the current assignment satisfies the addition equation."""
    # Convert letters to numbers
    def to_number(word):
        if not all(letter in assignment for letter in word):
            return None
        num = 0
        for letter in word:
            num = num * 10 + assignment[letter]
        return num
    
    num1 = to_number(operand1)
    num2 = to_number(operand2)
    num_result = to_number(result)
    
    # Check if numbers are valid and satisfy the equation
    if num1 is None or num2 is None or num_result is None:
        return False
    return num1 + num2 == num_result

def backtrack(assignment, letters, index, used_digits, leading_letters, operand1, operand2, result_word):
    """Backtracking to find a valid assignment of digits to letters."""
    if index == len(letters):
        # Check if the current assignment satisfies the equation
        if check_addition(assignment, operand1, operand2, result_word):
            return assignment
        return None
    
    letter = letters[index]
    # Try each available digit
    for digit in range(10):
        if digit not in used_digits:
            # Skip 0 for leading letters
            if digit == 0 and letter in leading_letters:
                continue
            # Trực tiếp sửa đổi assignment và used_digits
            assignment[letter] = digit
            used_digits.add(digit)
            
            # Recursively try next letter
            solution = backtrack(assignment, letters, index + 1, used_digits, 
                              leading_letters, operand1, operand2, result_word)
            if solution:
                return solution
                
            # Backtrack: remove assignment and digit
            del assignment[letter]
            used_digits.remove(digit)
    
    return None

def solve_cryptarithmetic(equation):
    """Solve the cryptarithmetic problem and return the solution."""
    try:
        operand1, operand2, result, letters, leading_letters = parse_input(equation)
    except ValueError as e:
        return "NO SOLUTION"
    
    # Initialize assignment dictionary and used digits set
    assignment = {}
    used_digits = set()
    
    # Start backtracking
    result_assignment = backtrack(assignment, letters, 0, used_digits, leading_letters, operand1, operand2, result)
    
    if result_assignment:
        # Format output: digits in alphabetical order of letters
        solution_string = ''.join(str(result_assignment[letter]) for letter in sorted(set(''.join(letters))))
        return solution_string
    else:
        return "NO SOLUTION"

def main():
    # Read input equation
    equation = input().strip()
    # Solve and print result
    print(solve_cryptarithmetic(equation))

if __name__ == "__main__":
    main()