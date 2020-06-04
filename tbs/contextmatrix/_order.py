__author__ = 'fbrucker'

__all__ = ["doubly_lexical_order", "is_doubly_lexically_ordered"]


def is_doubly_lexically_ordered(matrix):
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


def doubly_lexical_order(matrix, order=None):
    """Return a doubly lexical order.

    Uses a linear is the size of the matrix algorithm from Sprinrad (REF?).

    :param matrix: O/1 matrix
    :type matrix: list of list of 0/1 elements
    :param order: prefered line order. A list of lists

    If choice between rows, the largest one is taken first.

    :rtype: couple of line and column permutation
    """

    column_partition = ColumnBlock(range(len(matrix[0])))
    row_partition = None

    if order is None:
        row_partition = RowBlock(reversed(range(len(matrix))), column_partition)
    else:
        pred = None
        for x in order:
            row_partition = RowBlock(x, column_partition)
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
            row_has_not_only_1 = False
            column_subblock = current_column_block
            while column_subblock != end_column_block:
                for column in column_subblock.columns:
                    if matrix[row][column] == 0:
                        row_has_not_only_1 = True
                        common_columns = set(j for j in column_subblock.columns if matrix[row][j] == 1)
                        new_column = column_subblock.split(common_columns)
                        new_column.rows.append(row)
                        if new_column != column_subblock:
                            provoque_a_column_split = True
                        column_subblock = end_column_block
                        break
                if column_subblock != end_column_block:
                    column_subblock = column_subblock.pred
            if not row_has_not_only_1:
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
        self.rows = rows is not None and rows or list()

    def split(self, columns):
        """
        Split a block according to remaining rows.
        If a new block is created, it's attached to the left.

        Returns:
             New block if created, self otherwise.
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
        self.rows = list(rows)
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
                current_column_block.rows = list()
            current_column_block = current_column_block.pred
        if remaining_rows:
            rows_ordering.append((remaining_rows, end_column_block))

        for rows, column_block in rows_ordering[:-1]:
            self.add_pred(RowBlock(rows, column_block))
        self.rows = rows_ordering[-1][0]
        self.columns_block = rows_ordering[-1][1]
