__author__ = 'fbrucker'

__all__ = ["doubly_lexical_order", "is_doubly_lexical_ordered",
           "gamma_free_matrix", "gamma_free_matrix_bottom_up",
           "gamma_free_matrix_top_down",
           "context_matrix_approximation"]


def is_doubly_lexical_ordered(matrix):
    """Test if the matrix is doubly lexically ordered.

    :param matrix: O/1 matrix
    :type matrix: list of list of 0/1 elements

    :rtype: bool
    """
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] == 0:
                continue
            for j_next in range(j + 1, len(matrix[i])):
                if matrix[i][j_next] == 0:
                    line_ordered = False
                    for i_next in range(i + 1, len(matrix)):
                        if matrix[i_next][j] == 0 and matrix[i_next][j_next] == 1:
                            line_ordered = True
                            break
                    if not line_ordered:
                        return False
            for i_next in range(i + 1, len(matrix)):
                if matrix[i_next][j] == 0:
                    column_ordered = False
                    for j_next in range(j + 1, len(matrix[i])):
                        if matrix[i][j_next] == 0 and matrix[i_next][j_next] == 1:
                            column_ordered = True
                            break
                    if not column_ordered:
                        return False

    return True


def gamma_free_matrix(matrix, transform_to_gamma_free=False):
    return gamma_free_matrix_top_down(matrix, transform_to_gamma_free)


def gamma_free_matrix_top_down(matrix, transform_to_gamma_free=False):
    """ adds 1

    :param matrix:
    :param transform_to_gamma_free:
    :return:
    """
    was_gamma_free = True
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] == 1:
                i_next = i + 1
                while i_next < len(matrix) and matrix[i_next][j] == 0:
                    i_next += 1

                if i_next == len(matrix):
                    continue
                j_next = j + 1
                while j_next < len(matrix[i]) and matrix[i][j_next] == 0:
                    j_next += 1
                if j_next == len(matrix[i]):
                    continue

                if matrix[i_next][j_next] == 0:
                    was_gamma_free = False
                    if transform_to_gamma_free:
                        matrix[i_next][j_next] = 1
                    else:
                        return was_gamma_free

    return was_gamma_free


def gamma_free_matrix_bottom_up(matrix, transform_to_gamma_free=False):
    """ adds 0

    :param matrix:
    :param transform_to_gamma_free:
    :return:
    """
    was_gamma_free = True
    for i in range(len(matrix) - 1, -1, -1):
        j = 0
        while j < len(matrix[i]):
            if matrix[i][j] == 0:
                j += 1
                continue

            i_next = i + 1
            while i_next < len(matrix) and matrix[i_next][j] == 0:
                i_next += 1

            if i_next == len(matrix):
                j += 1
                continue

            j_next = j + 1
            while j_next < len(matrix[i]):
                while j_next < len(matrix[i]) and matrix[i][j_next] == 0:
                    j_next += 1

                if j_next == len(matrix[i]):
                    j_next = j + 1
                    break

                if matrix[i_next][j_next] == 0:
                    was_gamma_free = False
                    if transform_to_gamma_free:
                        matrix[i][j_next] = 0
                    else:
                        return was_gamma_free
                else:
                    break

            j = j_next
    return was_gamma_free


def context_matrix_approximation(context_matrix, approximation_method=gamma_free_matrix_top_down):
    """ return a new context_matrix DL ordered and gamma free and the line and column permutation
    new_context_matrix[i][j] == context_matrix[line_order[i]][column_order[j]]

    :param context_matrix:
    :param approximation_method: gamma_free_matrix_*
    :return:
    """

    approximation = context_matrix.copy()
    approximation.reorder_doubly_lexical_order()
    # import DLC.graphics

    # if_merdouille = DLC.graphics.raw_matrix(approximation.matrix)

    approximation_method(approximation.matrix, True)

    # if not gamma_free_matrix(approximation.matrix):
    #     print("--BIG MERDOUILLE---")
    #     print(if_merdouille)
    #     print("--------")

    approximation.reorder_doubly_lexical_order()

    return approximation


def doubly_lexical_order(matrix, order=None):
    """Return a doubly lexical order.

    :param matrix: O/1 matrix
    :type matrix: list of list of 0/1 elements

    If choice between rows, the smallest one is taken first.

    :rtype: couple of line and column permutation
    """
    column_partition = ColumnBlock(range(len(matrix[0])))
    if order is None:
        row_partition = RowBlock(range(len(matrix)), column_partition)
    else:
        pred = None
        for x in order:
            row_partition = RowBlock([x], column_partition)
            if pred is None:
                pred = row_partition
            else:
                pred.add_next(row_partition)
                pred = row_partition
    current_row_block = row_partition
    while current_row_block:
        current_column_block = current_row_block.columns_block
        end_column_block = current_column_block.pred
        full_one = set()
        provoque_a_column_split = False
        for row in current_row_block.rows:
            row_has_only_1 = False
            column_subblock = current_column_block
            while column_subblock != end_column_block:
                for column in column_subblock.columns:
                    if matrix[row][column] == 0:
                        row_has_only_1 = True
                        common_columns = set(j for j in column_subblock.columns if matrix[row][j] == 1)
                        new_column = column_subblock.split(common_columns)
                        new_column.rows.add(row)
                        if new_column != column_subblock:
                            provoque_a_column_split = True
                        column_subblock = end_column_block
                        break
                if column_subblock != end_column_block:
                    column_subblock = column_subblock.pred
            if not row_has_only_1:
                full_one.add(row)

        current_row_block.split(current_column_block, end_column_block, full_one)
        if not provoque_a_column_split:
            current_row_block.columns_block = current_column_block.pred

        if current_row_block.columns_block is None:
            current_row_block = current_row_block.pred

    return row_ordering_from_last_row_block(row_partition), column_ordering_from_last_column_block(column_partition)


def row_ordering_from_last_row_block(last_row_block):
    return ordering_from_last_node(last_row_block, lambda row_node: row_node.rows)


def column_ordering_from_last_column_block(last_column_block):
    return ordering_from_last_node(last_column_block, lambda column_node: column_node.columns)


def ordering_from_last_node(last_node, collect, sets=False):
    ordering = []
    current = last_node
    while current:
        if sets:
            ordering.append(collect(current))
        else:
            ordering.extend(collect(current))
        current = current.pred

    ordering.reverse()
    return ordering


class Node:
    def __init__(self):
        self.pred = None
        self.next = None

    def add_pred(self, node):
        node.next = self
        node.pred = self.pred
        if node.pred:
            node.pred.next = node
        self.pred = node

    def add_next(self, node):
        node.pred = self
        node.next = self.next
        if node.next:
            node.next.pred = node
        self.next = node


class ColumnBlock(Node):
    def __init__(self, columns, rows=None):
        super().__init__()
        self.columns = set(columns)
        self.rows = rows is not None and rows or set()

    def split(self, columns):
        """
        Split a block according to remaining rows.
        If a new block is created, it's attached to the left.

        :param last_column_bock: First rowBlock
        :param end_column_block: first block not to consider
        :param remaining_rows:

        :return: New block if created, self otherwise.
        """

        new_columns = self.columns - columns
        if new_columns and len(new_columns) < len(self.columns):
            new_block = ColumnBlock(new_columns)
            self.add_pred(new_block)
            self.columns -= new_columns
        else:
            new_block = self

        return new_block


class RowBlock(Node):
    def __init__(self, rows, columns_block=None):
        super().__init__()
        self.rows = set(rows)
        self.columns_block = columns_block

    def split(self, last_column_bock, end_column_block, remaining_rows):
        """
        Split a block according to remaining rows.
        If a new block is created, it's attached to the left.

        :param last_column_bock: First rowBlock
        :param end_column_block: first block not to consider
        :param remaining_rows:

        :return: New block if created, self otherwise.
        """
        current_column_block = last_column_bock
        rows_ordering = []
        while current_column_block != end_column_block:
            if current_column_block.rows:
                rows_ordering.append((current_column_block.rows, current_column_block))
                current_column_block.rows = set()
            current_column_block = current_column_block.pred
        if remaining_rows:
            rows_ordering.append((remaining_rows, end_column_block))

        for rows, column_block in rows_ordering[:-1]:
            self.add_pred(RowBlock(rows, column_block))
        self.rows = rows_ordering[-1][0]
        self.columns_block = rows_ordering[-1][1]


