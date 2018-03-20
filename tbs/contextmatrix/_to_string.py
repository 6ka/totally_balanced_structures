__author__ = 'francois'


def to_string(context_matrix,
              has_attribute="X", has_not_attribute=".",
              has_elements_label=True, has_attributes_label=True,
              sep=" "):
    """Context matrix string representation.

    :param context_matrix: context matrix to convert
    :type context_matrix: :class:`tbs.lattice.ContextMatrix`

    :param has_attribute: string to print when element has attribute
    :type has_attribute: :class:`str`

    :param has_not_attribute: string to print when element has not attribute
    :type has_not_attribute: :class:`str`

    :param has_elements_label: if first column is elements labels
    :type has_elements_label: :class:`bool`

    :param has_attributes_label: if first line is attributes names
    :type has_attributes_label: :class:`bool`

    :param sep: delimiter string
    :type sep: one caracter

    :rtype: :class:`str`
    """

    matrix = context_matrix.matrix
    objects_name = [str(x) for x in context_matrix.elements]
    attributes_name = [str(x) for x in context_matrix.attributes]

    if not objects_name:
        objects_name = [str(i) for i in range(len(matrix))]
    if not attributes_name:
        attributes_name = [str(i) for i in range(len(matrix[0]))]

    max_label = max([len(name) for name in objects_name]) + 1

    out = ""
    if has_attributes_label:
        out = sep.ljust(max_label)
        for j, name in enumerate(attributes_name):
            out += name.center(3)
            if j < len(attributes_name) - 1:
                out += sep

        out += "\n"

    for i, name in enumerate(objects_name):
        if has_elements_label:
            out += name.ljust(max_label)
        for j, attribute in enumerate(attributes_name):
            if matrix[i][j]:
                out += has_attribute.center(max(3, len(has_attribute), len(attribute)))
            else:
                out += has_not_attribute.center(max(3, len(has_not_attribute), len(attribute)))
            if j < len(attributes_name) - 1:
                out += sep
        out += "\n"
    return out
