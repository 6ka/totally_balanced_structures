__all__ = ["down_number_matrix", "up_number_matrix"]


def down_number_matrix(binary_matrix):
    """
    larger or equal to line
    :param binary_matrix:
    :return:
    """

    down, count = init_counters(len(binary_matrix[0]))

    for line in reversed(binary_matrix):
        add_line_true_to_count(line, count)
        down.append(list(count))

    down.reverse()

    return down


def init_counters(line_size):
    return [], [0] * line_size


def add_line_true_to_count(line, count):
    for index, element in enumerate(line):
        if element:
            count[index] += 1


def up_number_matrix(binary_matrix):
    """
    strictly smaller than line

    :param binary_matrix:
    :return:
    """

    up, count = init_counters(len(binary_matrix[0]))

    for line in binary_matrix:
        up.append(list(count))
        add_line_true_to_count(line, count)

    up.append(list(count))

    return up
