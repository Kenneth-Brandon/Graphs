def earliest_ancestor(ancestors, starting_node):
    ancestor_tree = {}

    for a in ancestors:
        parent = a[0]
        child = a[1]

        if child not in ancestor_tree:
            ancestor_tree[child] = [parent]
        else:
            ancestor_tree[child].append(parent)

    if starting_node not in ancestor_tree:
        return -1

    children = set([starting_node])
    parents = set()
    furthest_ancestor = False

    while not furthest_ancestor:
        for c in children:
            if c in ancestor_tree:
                for p in ancestor_tree[c]:
                    parents.add(p)

        if not parents:
            furthest_ancestor = True
            break

        children = parents
        parents = set()

    return min(children)
