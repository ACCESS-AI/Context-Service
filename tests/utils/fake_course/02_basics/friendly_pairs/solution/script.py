
def is_friendly_pair(num1, num2):

    # Check if num1 and num2 are natural numbers and they are not the same.
    # If conditions are not met return Invalid
    if not type(num1) == int or not type(num2) == int or num1 < 1 or num2 < 1 or num1 == num2:
        return "Invalid"

    # Find divisors of num1, calculate their sum and set it to teta1
    teta1 = sum([x for x in range(1,num1+1) if num1%x==0])
    # Find dividers of num2, calculate their sum and set it to teta2
    teta2 = sum([x for x in range(1,num2+1) if num2%x==0])

    # Calculate abundancy of number 1 by dividing teta1 by number 1
    abundancy1 = teta1 / num1
    # Calculate abundancy of number 2 by dividing teta2 by number 2
    abundancy2 = teta2 / num2

    # If both abundancies are equal num1 and num2 are a friendly pair
    return abundancy1 == abundancy2

