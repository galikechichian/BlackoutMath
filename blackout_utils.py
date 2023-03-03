#!/usr/bin/python3
# Author: Gali Kechichian

import math
import random

def do_op_for_numbers(op, num1, num2):
    '''(str, int, int) -> int
    Takes an operator op as as a string and 2 integers num1 and num2
    Returns the operation performed by op on num1 and num2
    
    >>> do_op_for_numbers('x', 3, 4)
    12
    
    >>> do_op_for_numbers('/', 6, 2)
    3
    
    >>> do_op_for_numbers('-', 1, 2)
    -1
    '''
    if op == '+':
        return num1 + num2
    elif op == '-':
        return num1 - num2
    elif op == 'x':
        return num1 * num2
    elif op == '/':
        if (num1 / num2) == math.inf:
            return 0;
        else:
            return num1 // num2
    elif op == '^':
        return num1 ** num2


def remove_from_list(my_list, indices):
    '''(list, list) -> list
    Takes 2 lists, my_list and indices and removes from my_list
    the elements at indixes given the elements of indices
    
    >>> remove_from_list(['The', 'quick', 'brown', 'fox'], [3, 2])
    ['quick', 'brown']
    
    >>> remove_from_list(['Hello', 'world'], [1, 0])
    []
    
    >>> remove_from_list(['Hello', 'world'], [5])
    ['Hello', 'world']
    '''
    res = []
    for i in range(len(my_list)):
        if i not in indices:
            res.append(my_list[i])
    return res


def find_last(my_list, x):
    '''(list, x) -> int
    Gives the index of the last element of the list
    which is equal to the second input
    
    >>> find_last(['a', 'b', 'b', 'a'], 'b')
    2

    >>> ind = find_last(['Hi', 'Hello'], 4)
    >>> print(ind)
    None
    
    >>> find_last(['Hi', 'Hello'], 'Hi')
    0
    '''
    i = len(my_list) - 1
    while i >= 0:
        if my_list[i] == x:
            return i
        i -= 1
    
    return None


def find_first(my_list, x):
    '''(list, x) -> int
    Gives the index of the first element of the list
    which is equal to the second input
    
    >>> find_last(['a', 'b', 'b', 'a'], 'b')
    1
    
    >>> ind = find_last(['abc', 'def'], False)
    >>> print(ind)
    None
    
    >>> find_first(['120', 50, 'hi', True, '120'], str(50+70))
    0
    '''
    if x in my_list:
        return my_list.index(x)
    return None


def generate_num_digits(pct_per_digit):
    '''(float) -> int
    Constructs an integer greater or equal to 1 by taking
    a float pct_per_digit and comparing it to a random float

    >>> random.seed(1337)
    >>> generate_num_digits(0)
    1
    
    >>> generate_num_digits(4392)
    1
    
    >>> random.seed(9)
    >>> generate_num_digits(0.649)
    5
    '''
    num = 1
    
    if pct_per_digit >= 1:  # the random percentage will never be greater than 1
        return num         # and so the loop would be infinite. it's a special case       
    
    random_percentage = random.random()
    while random_percentage < pct_per_digit:
        num += 1
        random_percentage = random.random()
    
    return num


def generate_number(pct_per_digit):
    '''(float) -> int
    Generates a random number with n digits depending on the float
    pct_per_digit provided as input
    
    >>> random.seed(1337)
    >>> generate_number(0)
    9
    
    >>> random.seed(800)
    >>> generate_number(0.9)
    17
    
    >>> generate_number(20)
    8
    '''
    num_digits = generate_num_digits(pct_per_digit) # length of the final number
    num = random.randint(10**(num_digits - 1), (10**(num_digits) - 1))
    return num


def check_equivalency(tokens):
    '''(list) -> bool
    Returns True if the list tokens has 3 elements, '=' as a second
    element and the first and third elements are equal to each other
    Returns False otherwiswe
    
    >>> check_equivalency([5, '=', 5, 'Hello'])
    False
    
    >>> check_equivalency([1, '=', 1])
    True
    
    >>> check_equivalency([4, 'x', 4])
    False
    '''
    return len(tokens) == 3 and tokens[1] == "=" and tokens[0] == tokens[2]
