def chordal_diss_from_fixed_order(diss, order):
    """modifiy diss to be chordal according to order"""

    for i in range(len(order)):
        x = order[i]
        for j in range(i + 1, len(order)):
            y = order[j]
            for k in range(j + 1, len(order)):
                z = order[k]

                if diss(y, z) > max(diss(x, y), diss(x, z)):
                    diss[y, z] = max(diss(x, y), diss(x, z))
