def trunc_float(float_val, int_pos, decimal_pos):
    int_value = int(float_val%(10**int_pos))
    print(int_value)
    decimal_value = int((float_val*10**decimal_pos)%(10**decimal_pos))
    print(decimal_value)
    return int_value + decimal_value*(10**(-decimal_pos))


print(trunc_float(1234.5678, 2, 3))