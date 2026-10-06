def get_large_numbers(numbers):
    result = []

    for x in numbers:
        if x > 5:
            result.append(x)

    return result


numbers = [2, 8, 4, 10, 5, 7]
print(get_large_numbers(numbers))