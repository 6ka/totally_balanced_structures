__all__ = ["order_by_map", "order_by_map_partition", "has_order_by_map"]


def order_by_map(vertices, vertices_map):
    final_order = []

    map_count = init_map_count(vertices, vertices_map)

    while map_count:
        v_star = min_map_count(map_count)
        final_order.append(v_star)
        update_map_count(v_star, map_count, vertices_map)

    return final_order


def order_by_map_partition(vertices, vertices_map):
    """

       Return a partition with all the min at the same time. If the min is always 0 for the vertices_map,
       the partition corresponds to a good order.  Results are unknown otherwise.

    Args:
        vertices:
        vertices_map:

    Returns:

    """

    final_order = []

    map_count = init_map_count(vertices, vertices_map)

    while map_count:
        v_star_set = all_min_map_count(map_count)
        final_order.append(v_star_set)
        for v_star in v_star_set:
            update_map_count(v_star, map_count, vertices_map)

    return final_order


def has_order_by_map(vertices, vertices_map):
    map_count = init_map_count(vertices, vertices_map)

    while map_count:
        v_star = min_map_count(map_count)
        if map_count[v_star] > 0:
            return False
        update_map_count(v_star, map_count, vertices_map)

    return True


def init_map_count(vertices, vertices_map):
    map_count = {x: 0 for x in vertices}
    for v in vertices:
        for x in vertices:
            for y in vertices:
                if x == y:
                    continue
                map_count[v] += vertices_map(v, x, y)
    return map_count


def min_map_count(map_count):
    return all_min_map_count(map_count).pop()


def all_min_map_count(map_count):

    v_star = set()
    min_v = None
    for v in map_count:
        if (not v_star) or (map_count[v] < min_v):
            v_star = {v}
            min_v = map_count[v]
        elif map_count[v] == min_v:
            v_star.add(v)

    return v_star


def update_map_count(v_star, map_count, vertices_map):
    del map_count[v_star]

    for v in map_count:
        map_count[v] -= 2 * sum(vertices_map(v, v_star, y) for y in map_count)
