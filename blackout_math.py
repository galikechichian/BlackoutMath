#!/usr/bin/python
# Author: Gali Kechichian
import random
from blackout_utils import *

OPERATIONS = ['^', 'x', '/', '+', '-']

def get_tokens_from_equation(line):
    '''(str) -> list
    Takes a string line containing a set of specific symbols and digits
    Returns a list of integers (the numbers) and strings (the symbols)
    
    >>> get_tokens_from_equation('653/=8+3')
    [653, '/', '=', 8, '+', 3]
    
    >>> get_tokens_from_equation('4=54+3/43-3x12')
    [4, '=', 54, '+', 3, '/', 43, '-', 3, 'x', 12]
    
    >>> get_tokens_from_equation('6-5=15^4/2')
    [6, '-', 5, '=', 15, '^', 4, '/', 2]
    
    '''
    # store all symbols in a string
    symbols = "+-x/=^()"

    result = []

    num = ""

    for char in line:
        if char in symbols:
            if num != "":
                result.append(int(num))
                num = ""
            result.append(char)
        else:
            num += char
    
    if num != "":
        result.append(int(num))

    return result


def process_operations(ops, tokens):
    '''(list, list) -> list
    Takes mathematical operations (ops) and tokens
    and returns a new list with the result of the operations
    
    >>> process_operations(['x'], [5, 'x', 7, '+', 2])
    [35, '+', 2]
    
    >>> process_operations(['/'], [54, '^', '+', 3])
    [54, '^', '+', 3]
    
    >>> process_operations(['x','y'], [15, 'x', 12, '/', 6])
    [180, '/', 6]
    '''
    result = tokens
    for op in ops:
        if op in OPERATIONS:
            for i in range(len(tokens)):
                section = result[i-1:i+2]
                if (len(section) < 3) or (section[1] != op) or (type(section[0]) != int) or (type(section[2]) != int):
                    continue
                else:
                    op = section[1]
                    num1 = section[0]
                    num2 = section[2]
                    computed_num = do_op_for_numbers(op, num1, num2)
                    result[i] = computed_num
                    result = remove_from_list(result, [i-1, i+1])
    return result

    
def get_ops(tokens):
    ops = []
    for token in tokens:
        if (token in OPERATIONS) and (token not in ops):
            # highest precedence
            if token == '^':
                ops = [token] + ops
            # careful here:
            elif token == 'x' or token == '/':
                if len(ops) == 0 or (len(ops) == 1 and ops[0] in ['^', 'x', '/']):
                    ops.append(token)
                elif ops[0] in ['+', '-']:
                    ops = [token] + ops
                else:
                    for i in range(len(ops)):
                        if ops[i] in ['+', '-']:
                            before = ops[:i]
                            after = ops[i:]
                            ops = before + [token] + after
                            break
            # either + or -, easy
            else:
                ops.append(token)
    return ops


def remove_parentheses(tokens):
    while '(' in tokens:
        start = find_last(tokens, '(')
        end = find_first(tokens, ')')
        if (start > end): # 2 or more parenthesed expressions that aren't nested
            end = 'dummy value'
            for i in range(start, len(tokens)):
                if tokens[i] == ')':
                    end = i
                    break
            before = tokens[:start]
            after = tokens[end+1:]

            to_process = tokens[start:end+1]
            ops = get_ops(to_process)
            processed = process_operations(ops, to_process)

            tokens = before + processed + after
            tokens = remove_from_list(tokens, [find_last(tokens, '('), find_last(tokens, ')')])

        else:
            before = tokens[:start]
            after = tokens[end+1:]

            to_process = tokens[start:end+1]
            ops = get_ops(to_process)
            processed = process_operations(ops, to_process)

            tokens = before + processed + after

            opening = find_last(tokens, '(')
            closing = find_first(tokens, ')')

            tokens = remove_from_list(tokens, [opening, closing])

    return tokens


def calculate(tokens):
    '''(list) -> list
    Takes a list of tokens
    Returns a a list with the result of the left-hand side,
    the equals sign and the result of the right-hand side
    
    >>> calculate([4, 'x', 2, '=', 9, 'x', 2])
    [8, '=', 18]
    
    >>> calculate([5, 'x', '(', 4, '+', 2, ')', '=', 49])
    [30, '=', 49]
    
    >>> calculate([4, '+', '-', 8])
    [4, '+', '-', 8]
    
    >>> calculate([3, 'x', 'x', 7])
    [3, 'x', 'x', 7]
    '''
    # initialize left hand side and right hand side in 2 seperate variables
    lhs = []
    rhs = []
    for i in range(len(tokens)):
        if tokens[i] == '=':
            lhs = tokens[:i]
            rhs = tokens[i+1:]
            break

    # check for '=' sign
    if lhs == [] or rhs == []:
        return tokens

    # check for balanced parentheses in both sides
    num_opening_parentheses_tokens = 0
    num_closing_parentheses_tokens = 0
    for token in lhs:
        if token == '(':
            num_opening_parentheses_tokens += 1
        if token == ')':
            num_closing_parentheses_tokens += 1
            
    num_opening_parentheses_rhs = 0
    num_closing_parentheses_rhs = 0
    for token in rhs:
        if token == '(':
            num_opening_parentheses_rhs += 1
        if token == ')':
            num_closing_parentheses_rhs += 1

    tokens_parentheses_balanced = num_opening_parentheses_tokens == num_closing_parentheses_tokens
    rhs_parentheses_balanced = num_opening_parentheses_rhs == num_closing_parentheses_rhs
    if not tokens_parentheses_balanced or not rhs_parentheses_balanced:
        return tokens

    # get rid of parentheses
    lhs = remove_parentheses(lhs)
    rhs = remove_parentheses(rhs)

    # no parentheses, just operators and precedence
    ops_lhs = get_ops(lhs)
    ops_rhs = get_ops(rhs)

    lhs = process_operations(ops_lhs, lhs)
    rhs = process_operations(ops_rhs, rhs)

    return lhs + ['='] + rhs


def brute_force_blackout(exp):
    '''(str) -> list
    '''
    # clean up the spaces in exp
    i = 0
    while i < len(exp):
        if exp[i] == ' ':
            before = exp[:i]
            after = exp[i+1:]
            exp = before + after
        i += 1

    for i in range(len(exp)):
        exclude_one = exp[:i] + exp[i+1:]
        for j in range(len(exp)):
            exclude_two = exclude_one[:j] + exclude_one[j+1:]
            tokens = get_tokens_from_equation(exclude_two)
            result = calculate(tokens)

            if check_equivalency(result):
                return exclude_two


def create_equation(n, pct_per_digit):
    '''
    '''
    my_list = []
    if n%2==0:
        n=n-1
    
    my_list.append(generate_number(pct_per_digit))

    for i in range(1,n):
        if i%2==0 or i == n-1:
            my_list.append(generate_number(pct_per_digit))
        else: # odd index
            my_list.append(OPERATIONS[random.randint(0, 4)])
    
    eq_index = random.randint(1,n-1)
    while my_list[eq_index] not in OPERATIONS and my_list[eq_index] != '=':
        eq_index = random.randint(1,n-1)
    my_list[eq_index] = '='
    return my_list


def find_solvable_blackout_equation(num_tries, n, pct_per_digit):
    '''(int, int, float) -> list
    Randomly creates and returns a solvable Blackout Math
    equation of length n and with each number having pct_per_digit
    to have more than one digit.
    It takes num_tries amount of tries to generate an equation
    
    >>> random.seed(42)
    >>> find_solvable_blackout_equation(1000, 7, 0.2)
    [37, '+', 9, '=', 1, 'x', 6]

    '''
    for i in range (num_tries):
        result = create_equation(n, pct_per_digit)
        for i in range(len(result)):
            if result[i] != '=':
                for j in range(len(result)):
                    if result[j] != '=':
                        newResult = calculate(remove_from_list(result, [i, j]))
                        if check_equivalency(newResult):
                            return result

    return None


def menu():
    '''() -> NoneType
    Lets the user either to create a Blackout Math equation
    or to solve one
    
    >>> Welcome to Blackout Math!
    Please choose from the following:
         1        Solve equation
         2        Create equation
    Your choice: 1
    Please enter the equation without spaces: 6-5=15^4/2 Solution found: [6, '-', 5, '=', 1, '^', 42]
    Have a nice day! 
    >>>
    
    '''
    print('Welcome to Blackout Math!')
    print('Please choose from the following:')
    print('1\tSolve equation')
    print('2\tCreate equation')
    choice = int(input("Your choice: "))

    if choice == 1:
        equation = str(input('Please enter the equation without spaces: '))
        solution = brute_force_blackout(equation)
        if solution == None:
            print('No solution found.')
        else:
            print('Solution found:', solution)
        print('Have a nice day!')

    elif choice == 2:
        tries = int(input('Enter number of tries: '))
        length = int(input('Enter length: '))
        prct = float(input('Enter % of additional digit: '))
        equation = find_solvable_blackout_equation(tries,length, prct)
        if equation == None:
            print('No equation could be generated with the given inputs.')
        else:
            print('Equation:', equation)
        print('Have a nice day!')

    else:
        print('Invalid choice')
        print('Have a nice day!')


menu()
