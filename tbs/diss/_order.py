def min(d, element_subset=None, indices=False, xx=False, index=False):
    """Minimal value on *Y*.

    :param element_subset: subset of base set. Considered to be the base set if ``None``
    :type element_subset: iterable

    :param indices: only the minimum or also the pair realizing this minimum.
    :type indices: :class:`bool`

    :param index: if True the *f* function works on the indices rather on the
                  elements of *X*
    :type index: :class:`bool`

    :param xx: considering *self*\ (x, x) values or not (by default, not).
    :type xx:  :class:`bool`

    :returns: Returns the minimum value on *Y* if *indices* is :const:`False` a
              :class:`dict` = {``'x'``: *minx*, ``'y'``: *miny*, ``'min'``:*value*}
              where self(*minx*, *miny*) = *value*.

    :rtype: a value or a :class:`dict`.
    """

    mind = None
    minx = None
    miny = None

    if not element_subset:
        element_subset = list(d)
    elif len(element_subset) == 1:
        element_subset = list(element_subset)
        x = element_subset[0]
        mind = d(x, x)
        minx = x
        miny = x
    else:
        element_subset = list(element_subset)

    if index:
        dist = lambda u, v: d.get_by_pos(u, v)
    else:
        dist = lambda u, v: d(u, v)

    for i, x in enumerate(element_subset):
        for y in element_subset[i:]:
            if x != y or xx:
                if mind is None or mind > dist(x, y):
                    minx = x
                    miny = y
                    mind = dist(x, y)

    if not indices:
        return mind
    else:
        return {'x': minx,
                'y': miny,
                'min': mind}


def max(d, element_subset=None, indices=False, xx=False, index=False):
    """Maximal value on Y

    :param element_subset: subset of base set. Considered to be the base set if  ``None``.
    :type element_subset: iterable

    :param indices: only the maximum or also the pair realizing this maximum.
    :type indices: :class:`bool`

    :param index: if True the *f* function works on the indices rather on the
                  elements of *X*
    :type index: :class:`bool`

    :param xx: considering *self*\ (x, x) values or not (by default, not).
    :type xx:  :class:`bool`

    :returns: Returns the maximum value on *Y* if *indices* is :const:`False` a
              :class:`dict` = {``'x'``: *maxx*, ``'y'``: *maxy*, ``'max'``: *value*}
              where self(*maxx*, *maxy*) = *value*.

    :rtype: a value or a :class:`dict`.
    """

    maxd = None
    maxx = None
    maxy = None

    if not element_subset:
        element_subset = list(d)
    elif len(element_subset) == 1:
        element_subset = list(element_subset)
        x = element_subset[0]
        maxd = d(x, x)
        maxx = x
        maxy = x
    else:
        element_subset = list(element_subset)

    if index:
        def dist(u, v):
            return d.get_by_pos(u, v)
    else:
        def dist(u, v):
            return d(u, v)

    for i, x in enumerate(element_subset):
        for y in element_subset[i:]:
            if x != y or xx:
                if maxd is None or maxd < dist(x, y):
                    maxx = x
                    maxy = y
                    maxd = dist(x, y)

    if not indices:
        return maxd
    else:
        return {'x': maxx,
                'y': maxy,
                'max': maxd}


def rank(d, element_subset=None):
    """Value ranks.

    :param element_subset: subset of base set. Considered to be the base set if  ``None``.
    :type element_subset: iterable

    :returns: a :class:`dict` `r` whose keys are the elements of `Y` and values
              a dict also taken its keys in Y. r[x][y] is the rank of y for x
              (d(x, y) is the r[x][y] smallest value of {d(x, y) | y in Y}).
              By convention, rank begins at 0.
    """

    if not element_subset:
        element_subset = list(d)
    else:
        element_subset = list(element_subset)

    r = dict()
    for x in element_subset:
        r[x] = dict()
        elems = list(element_subset)
        elems.sort(key=lambda u: d(x, u))
        pos = 0
        value = d(x, elems[0])
        for y in elems:
            if d(x, y) != value:
                value = d(x, y)
                pos += 1
            r[x][y] = pos
    return r
