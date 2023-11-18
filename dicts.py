"""Functions dealing with dictionaries."""

import graphviz


def invert(d: dict) -> dict:
    """
    Invert the dictionary.

    If the dict is not injective an arbitrary choice is made.

    >>> invert({"one": 1, "pi": 3, "tau": 6.283185307179586})
    {1: 'one', 3: 'pi', 6.283185307179586: 'tau'}
    >>> invert({})
    {}
    """
    inv_d = {}
    for key, value in d.items():
        inv_d[value] = key
    return inv_d


def sorted_al(adj_list: dict[str,set[str]]) -> dict[str,list[str]]:
    """
    Sort an adjacency list.

    This takes an adjacency list represented as a dictionary whose keys are
    vertices and whose values are sets of their outward neighbors, and returns
    a new, similar dictionary whose values are instead sorted lists.
    """
    sl = {}
    for vertex, neighbors in adj_list.items():
        sl[vertex] = sorted(neighbors)
    return sl


def adjacency(edges: list[tuple[str,str]]) -> dict[str,set[str]]:
    """
    Make an adjacency list.

    This takes edges expressed as pairs of source and destination vertices, and
    return an adjacency list as a dictionary whose keys are vertices and whose
    values are sets of their outward neighbors.

    >>> adjacency([])
    {}
    >>> adjacency([('a', 'A')])
    {'a': {'A'}}
    >>> adjacency([('a','b'), ('b','c'), ('c','a')])
    {'a': {'b'}, 'b': {'c'}, 'c': {'a'}}
    >>> sorted_al(adjacency([('a','c'), ('a','b'), ('b','c'), ('c','a')]))
    {'a': ['b', 'c'], 'b': ['c'], 'c': ['a']}
    """
    adj_list = {}
    for source, dest in edges:
        if source in adj_list:
            adj_list[source].add(dest)
        else:
            adj_list[source] = {dest}
    return adj_list


# TODO: The parameter annotation is too narrow. Use abstract types instead.
def draw_graph(adj_list: dict[str,set[str]]) -> graphviz.Digraph:
    R"""
    Draw a directed graph.

    >>> graph = draw_graph({'a': {'b', 'c'}, 'b': {'c'}, 'c': {'a'}})
    >>> str(graph) in {
    ...     'digraph {\n\ta -> b\n\ta -> c\n\tb -> c\n\tc -> a\n}\n',
    ...     'digraph {\n\ta -> c\n\ta -> b\n\tb -> c\n\tc -> a\n}\n',
    ... }
    True
    >>> print(draw_graph({1: {2}}))  # doctest: +NORMALIZE_WHITESPACE
    digraph {
        1 -> 2
    }
    """
    g = graphviz.Digraph()
    for source,targets in adj_list.items():
        for dest in targets:
            g.edge(str(source),str(dest))
    return g


def sorted_setoset(unsorted: set[frozenset]) -> list[list]:
    unsorted_list = []
    for collection in unsorted:
        unsorted_list.append(sorted(collection))
    return sorted(unsorted_list)


def components_quickfind(edges: list[tuple[str,str]]) -> set[frozenset[str]]:
    """
    Identify the connected components from an edge list.

    >>> components_quickfind([])
    set()
    >>> sorted_setoset(components_quickfind( [ ('1','2'), ('1','3'), ('4','5'), ('5','6'), ('3','7'), ('2','7') ] ))
    [['1', '2', '3', '7'], ['4', '5', '6']]
    """
    # Make singleton sets.
    sets = {vertex: [vertex] for edge in edges for vertex in edge}

    def join(to_set: list[str], from_set: list[str]) -> None:
        for vertex in from_set:
            sets[vertex] = to_set
        to_set.extend(from_set)

    # Unite each edge's endpoints' sets by size, melding smaller into larger.
    for u, v in edges:
        u_set = sets[u]
        v_set = sets[v]

        if u_set is v_set:
            continue

        if len(u_set) < len(v_set):
            join(v_set, u_set)
        else:
            join(u_set, v_set)

    sets_by_id = {id(component): component for component in sets.values()}
    return {frozenset(component) for component in sets_by_id.values()}


def components_quickfind_classic(edges: list[tuple[str,str]]) -> set[frozenset[str]]:
    """
    Identify the connected components from an edge list.

    This uses classic quick-find (with representative elements), in contrast to
    components(), which is also quick-find but uses list references themselves.

    >>> components_quickfind_classic([])
    set()
    >>> sorted_setoset(components_quickfind_classic( [ ('1','2'), ('1','3'), ('4','5'), ('5','6'), ('3','7'), ('2','7') ] ))
    [['1', '2', '3', '7'], ['4', '5', '6']]
    """
    # Make singleton sets.
    representatives = {vertex: vertex for edge in edges for vertex in edge}
    chains = {vertex: [vertex] for vertex in representatives}

    def join(to_vertex: str, from_vertex: str) -> None:
        for vertex in chains[from_vertex]:
            representatives[vertex] = to_vertex
        chains[to_vertex].extend(chains[from_vertex])

    # Unite each edge's endpoints' sets by size, melding smaller into larger.
    for u, v in edges:
        u = representatives[u]
        v = representatives[v]

        if u == v:
            continue

        if len(chains[u]) < len(chains[v]):
            join(v, u)
        else:
            join(u, v)

    canonical_vertices = set(representatives.values())
    return {frozenset(chains[vertex]) for vertex in canonical_vertices}


def components_quickunion(edges: list[tuple[str,str]]) -> set[frozenset[str]]:
    """
    Identify the connected components from an edge list.

    This uses quick-union, also known as union by rank.

    >>> components_quickunion([])
    set()
    >>> sorted_setoset(components_quickunion( [ ('1','2'), ('1','3'), ('4','5'), ('5','6'), ('3','7'), ('2','7') ] ))
    [['1', '2', '3', '7'], ['4', '5', '6']]
    """
    # Make singleton sets.
    parents = {vertex: vertex for edge in edges for vertex in edge}
    ranks = {vertex: 0 for vertex in parents}

    def find(elem: str) -> str:
        while elem != parents[elem]:
            elem = parents[elem]
        return elem

    # Unite each edge's endpoints' sets by rank.
    for u, v in edges:
        u = find(u)
        v = find(v)

        if u == v:
            continue

        if ranks[u] < ranks[v]:
            parents[u] = v
        else:
            if ranks[u] == ranks[v]:
                ranks[u] += 1
            parents[v] = u

    sets_by_ancestor = {}

    for vertex in parents:
        ancestor = find(vertex)
        try:
            sets_by_ancestor[ancestor].append(vertex)
        except KeyError:
            sets_by_ancestor[ancestor] = [vertex]

    return {frozenset(component) for component in sets_by_ancestor.values()}
