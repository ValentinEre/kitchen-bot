def get_cool_id(first, second):
    if len(first) == len(second):
        list_diff = []
        for num in first:
            index_in_first = first.index(num)
            index_in_second = second.index(num)
            difference = abs(index_in_first - index_in_second)
            list_diff.append(difference)
        print(list_diff)
    else:
        raise ValueError("Lists of different length.")

    return first[list_diff.index(min(list_diff))]

#
# a = []
# b = []
#
# for ind in range(10):
#     a.append(ind)
#     b.append(ind)
#
# shuffle(a)
# shuffle(b)
# print(f'{a}\n{b}\n')
# print(differences(first=a, second=b))
