# Trình giải bài toán Cryptarithmetic cho các phương trình như ABCD - EFGH = IJ
# Sử dụng backtracking với kiểm tra ràng buộc để tránh brute force

def parse_input(equation):
    """Phân tích chuỗi đầu vào (ví dụ: 'ABCD-EFGH=IJ') để trích xuất toán hạng, toán tử và kết quả."""
    # Loại bỏ khoảng trắng thừa
    equation = equation.replace(" ", "")
    
    # Kiểm tra xem phương trình có chứa dấu '=' không
    if '=' not in equation:
        raise ValueError("Input must contain '='")
    
    # Tách phương trình thành bên trái (toán hạng) và bên phải (kết quả)
    parts = equation.split('=')
    if len(parts) != 2:
        raise ValueError("Input must have exactly one '='")
    left_side, right = parts
    
    # Kiểm tra toán tử '+' hoặc '-'
    if '+' in left_side:
        operator = '+'
        operand_parts = left_side.split('+')
    elif '-' in left_side:
        operator = '-'
        operand_parts = left_side.split('-')
    else:
        raise ValueError("Input must contain '+' or '-' in the left side")
    
    # Tách bên trái thành hai toán hạng
    if len(operand_parts) != 2:
        raise ValueError("Left side must have exactly two operands separated by '+' or '-'")
    operand1, operand2 = operand_parts
    
    # Kiểm tra xem toán hạng và kết quả có chứa chỉ chữ in hoa không
    if not (operand1.isupper() and operand2.isupper() and right.isupper()):
        raise ValueError("Operands and result must contain only uppercase letters")
    
    # Lấy các chữ cái duy nhất theo thứ tự bảng chữ cái
    letters = sorted(set(operand1 + operand2 + right))
    # Xác định các chữ cái dẫn đầu (không được là 0)
    leading_letters = {operand1[0], operand2[0], right[0]}
    return operand1, operand2, right, letters, leading_letters, operator

def check_equation(assignment, operand1, operand2, result, operator):
    """Kiểm tra xem gán hiện tại có thỏa mãn phương trình không."""
    # Chuyển đổi chữ cái thành số
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
    
    # Kiểm tra xem các số có hợp lệ không
    if num1 is None or num2 is None or num_result is None:
        return False
    
    # Kiểm tra phương trình dựa trên toán tử
    if operator == '+':
        return num1 + num2 == num_result
    elif operator == '-':
        return num1 - num2 == num_result
    return False

def backtrack(assignment, letters, index, used_digits, leading_letters, operand1, operand2, result_word, operator):
    """Sử dụng backtracking để tìm gán hợp lệ của các chữ số cho các chữ cái."""
    if index == len(letters):
        # Kiểm tra xem gán hiện tại có thỏa mãn phương trình không (Điểm khác so với khi dùng Brute Force)
        if check_equation(assignment, operand1, operand2, result_word, operator):
            return assignment
        return None
    
    letter = letters[index]
    # Thử từng chữ số có sẵn
    for digit in range(10):
        if digit not in used_digits:
            # Bỏ qua số 0 cho các chữ cái dẫn đầu (ràng buộc (constraint))
            if digit == 0 and letter in leading_letters:
                continue
            # Gán chữ số cho chữ cái
            assignment[letter] = digit
            used_digits.add(digit)
            
            # Đệ quy thử chữ cái tiếp theo
            solution = backtrack(assignment, letters, index + 1, used_digits, 
                                leading_letters, operand1, operand2, result_word, operator)
            if solution:
                return solution
                
            # Quay lui: xóa gán và chữ số (Backtrack)
            del assignment[letter]
            used_digits.remove(digit)
    
    return None

def solve_cryptarithmetic(equation):
    """Giải bài toán cryptarithmetic và trả về kết quả."""
    try:
        operand1, operand2, result, letters, leading_letters, operator = parse_input(equation)
    except ValueError:
        return "NO SOLUTION"
    
    # Khởi tạo từ điển gán và tập hợp các chữ số đã sử dụng
    assignment = {}
    used_digits = set()
    
    # Bắt đầu backtracking
    result_assignment = backtrack(assignment, letters, 0, used_digits, leading_letters, operand1, operand2, result, operator)
    
    if result_assignment:
        # Định dạng đầu ra: các chữ số theo thứ tự bảng chữ cái của các chữ cái
        solution_string = ''.join(str(result_assignment[letter]) for letter in sorted(set(''.join(letters))))
        return solution_string
    else:
        return "NO SOLUTION"

def main():
    # Đọc phương trình đầu vào
    equation = input().strip()
    # Giải và in kết quả
    print(solve_cryptarithmetic(equation))

if __name__ == "__main__":
    main()