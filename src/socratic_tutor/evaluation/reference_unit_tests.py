"""Reference unit tests copied from the original notebook's evaluation section."""

unit_tests = {
    "factorial": '''assert factorial(0) == 1
assert factorial(1) == 1
assert factorial(5) == 120
assert factorial(-2) == "OOPS"''',
    "gcd": '''assert gcd(12,18) == 6
assert gcd(100,25) == 25
assert gcd(7,3) == 1
assert gcd(0,5) == 5''',
    "remove_duplicates": '''assert remove_duplicates([1,2,2,3]) == [1,2,3]
assert remove_duplicates([]) == []
assert remove_duplicates([5,5,5]) == [5]''',
    "palindrome": '''assert palindrome("Racecar") == True
assert palindrome("hello") == False
assert palindrome("") == True''',
    "sum_even": '''assert sum_even([1,2,3,4]) == 6
assert sum_even([2,4,6]) == 12
assert sum_even([1,3,5]) == 0''',
    "fibonacci": '''assert fibonacci(1) == 1
assert fibonacci(2) == 1
assert fibonacci(5) == 5
assert fibonacci(10) == 55
assert fibonacci(0) == "OOPS"''',
    "sum_squares": '''assert sum_squares([1,2,3]) == 14
assert sum_squares([0,4,5]) == 41
assert sum_squares([]) == 0''',
    "has_duplicates": '''assert has_duplicates([1,2,3,2]) == True
assert has_duplicates([1,2,3]) == False
assert has_duplicates([]) == False''',
    "sum_list": '''assert sum_list([1,2,3]) == 6
assert sum_list([]) == 0''',
    "reverse_words": '''assert reverse_words("hello world") == "world hello"
assert reverse_words("I love Python") == "Python love I"
assert reverse_words("") == ""''',
    "reverse_string": '''assert reverse_string("hello") == "olleh"
assert reverse_string("") == ""''',
    "is_prime": '''assert is_prime(1) == False
assert is_prime(2) == True''',
    "max_in_list": '''assert max_in_list([1,5,2]) == 5
assert max_in_list([0,-1,-5]) == 0
assert max_in_list([42]) == 42''',
    "count_vowels": '''assert count_vowels("Apple") == 2
assert count_vowels("HELLO") == 2
assert count_vowels("") == 0''',
    "reverse_list": '''assert reverse_list([1,2,3]) == [3,2,1]
assert reverse_list([]) == []''',
    "fibonacci_sum": '''assert fibonacci_sum(1) == 1
assert fibonacci_sum(2) == 2
assert fibonacci_sum(5) == 7''',
    "factorial_iter": '''assert factorial(0) == 1
assert factorial(1) == 1
assert factorial(5) == 120
assert factorial(-2) == "OOPS"''',
}
