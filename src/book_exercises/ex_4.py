def hex_output(hex_string):
    int_value = 0
    i = 0
    for char in reversed(hex_string[2:]):
        int_value += int(char, 16)*16**i
        i += 1
    return int_value


print(hex_output('0xFF'))
