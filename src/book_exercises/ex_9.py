# def firstlast(seq):
#     """
#     Takes a sequence (string, list, or tuple) and returns the first and last elements of that sequence,
#     in a sequence of the same type.
#     """
#     first, last = seq[0], seq[-1]
#     if type(seq) is str:
#         return first + last
#     elif type(seq) is list:
#         return [first, last]
#     elif type(seq) is tuple:
#         return first, last
#     else:
#         return None

def firstlast(sequence):
    return sequence[:1] + sequence[-1:]


print(firstlast('abcde'))
print(firstlast([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]))
print(firstlast((9, 8, 7, 6, 5, 4, 3, 2, 1)))
