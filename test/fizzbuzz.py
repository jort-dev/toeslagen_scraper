"""
The FizzBuzz problem is a simple programming challenge that typically goes like this:

Write a program that prints the numbers from 1 to 100. However:

For multiples of 3, print "Fizz" instead of the number.
For multiples of 5, print "Buzz" instead of the number.
For numbers which are multiples of both 3 and 5, print "FizzBuzz" instead of the number.
It's a common interview question used to assess basic programming logic and control flow understanding.
"""

for number in range(1, 101):
    if number % 3 == 0:
        print("Fizz")
    else:
        print(number)
    if number % 5 == 0:
        print("Buzz")
    else:
        print(number)
