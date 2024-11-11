def sum_digits(number):
    number_str = str(number)

    total_sum = 0

    for i in number_str:
        total_sum += int(i)

    return total_sum

print(sum_digits(12345))