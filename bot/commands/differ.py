def same_len_list(
        first, second
):
    set_first = set(first)
    set_second = set(second)
    diff = set_first.difference(set_second)

    diff_list = list(diff)
    second = diff_list + second
    return second


def get_cool_id(first, second):
    list_diff = []
    if len(first) == len(second):

        for num in first:
            index_in_first = first.index(num)
            index_in_second = second.index(num)
            difference = abs(index_in_first - index_in_second)
            list_diff.append(difference)
        print(list_diff)

    return first[list_diff.index(min(list_diff))]
