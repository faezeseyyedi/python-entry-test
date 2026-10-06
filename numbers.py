def get_large_numbers(numbers):
    result = []

    for x in numbers:
        if x > 10:
            result.append(x)

    return result

numbers = [3, 8, 12, 5, 7, 20]
print(get_large_numbers(numbers))