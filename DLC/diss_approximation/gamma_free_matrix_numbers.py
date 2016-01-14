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


def columns_as_truncated_balls(binary_matrix):
    up_count = up_number_matrix(binary_matrix)
    down_count = down_number_matrix(binary_matrix)

    truncated_balls = []
    for i, line in enumerate(binary_matrix):
        last_size = 0
        for j, element in enumerate(line):
            if element and up_count[i][j] == 0 and down_count[i][j] > last_size:
                last_size = down_count[i][j]
                truncated_balls.append((i, j))

    return truncated_balls
