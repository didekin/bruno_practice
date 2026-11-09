import decimal as dec

dec.getcontext().prec = 3


def sum_decimal():
    ast, bst = input("Enter two float numbers with a space between them: ").strip().split()
    return dec.Decimal(ast) + dec.Decimal(bst)


print(sum_decimal())