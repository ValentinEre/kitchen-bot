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
    inverse_index = {element: index for index, element in enumerate(first)}
    my_list = [inverse_index[element]
               for index, element in enumerate(second) if element in inverse_index]
    return first[my_list.index(min(my_list))]

