"""Functions dealing with dictionaries."""

import collections
from collections.abc import Callable, Iterable

import graphviz

from util import identity_function


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


def distinct(values: Iterable, *, key=None) -> list:
    """
    Create a list with every value of the values, but without repeating any.

    >>> distinct([])
    []
    >>> distinct([3,6,123,1,543,1,32,1,3,3,12])
    [3, 6, 123, 1, 543, 32, 12]
    >>> distinct([ {1,2}, {1}, {2,2,1}, {2}, {1,1,1}], key=frozenset)
    [{1, 2}, {1}, {2}]
    """
    if key is None:
        key = identity_function

    val_list = []
    val_set = set()

    for val in values:
        if key(val) not in val_set:
            val_set.add(key(val))
            val_list.append(val)
    return val_list


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


def adjacency(
    edges: list[tuple[str,str]],
    vertices: Iterable[str] = (),
    *,
    directed: bool = True,
) -> dict[str,set[str]]:
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
    >>> adjacency([('a','b'), ('b','c'), ('c','a')], ('d','a','e'))
    {'a': {'b'}, 'b': {'c'}, 'c': {'a'}, 'd': set(), 'e': set()}

    >>> adjacency([], directed=False)
    {}
    >>> adjacency([('a', 'A')], directed=False)
    {'a': {'A'}, 'A': {'a'}}
    >>> sorted_al(adjacency([('a','b'), ('b','c'), ('c','a')], directed=False))
    {'a': ['b', 'c'], 'b': ['a', 'c'], 'c': ['a', 'b']}
    >>> sorted_al(adjacency([('a','c'), ('a','b'), ('b','c'), ('c','a')],
    ...                     directed=False))
    {'a': ['b', 'c'], 'c': ['a', 'b'], 'b': ['a', 'c']}
    >>> sorted_al(adjacency([('a','b'), ('b','c'), ('c','a')], ('d','a','e'),
    ...                     directed=False))
    {'a': ['b', 'c'], 'b': ['a', 'c'], 'c': ['a', 'b'], 'd': [], 'e': []}
    """
    adj_list = {}

    for source, dest in edges:
        if source in adj_list:
            adj_list[source].add(dest)
        else:
            adj_list[source] = {dest}

        if not directed:
            if dest in adj_list:
                adj_list[dest].add(source)
            else:
                adj_list[dest] = {source}

    for vertex in vertices:
        if vertex not in adj_list:
            adj_list[vertex] = set()

    return adj_list


# NOTE: adjacency() covers this. So this might be removed.
def adjacency_undirected(edges: list[tuple[str,str]]) -> dict[str,set[str]]:
    """
    Make an adjacency list for an undirected graph.

    >>> adjacency_undirected([])
    {}
    >>> adjacency_undirected([('a', 'A')])
    {'a': {'A'}, 'A': {'a'}}
    >>> sorted_al(adjacency_undirected([('a','b'), ('b','c'), ('c','a')]))
    {'a': ['b', 'c'], 'b': ['a', 'c'], 'c': ['a', 'b']}
    >>> edges = [('a','c'), ('a','b'), ('b','c'), ('c','a')]
    >>> sorted_al(adjacency_undirected(edges))
    {'a': ['b', 'c'], 'c': ['a', 'b'], 'b': ['a', 'c']}
    >>> sorted_al(adjacency_undirected([('a', 'b'), ('c', 'b'), ('d', 'a')]))
    {'a': ['b', 'd'], 'b': ['a', 'c'], 'c': ['b'], 'd': ['a']}
    """
    adj = collections.defaultdict(set)
    for u, v in edges:
        adj[u].add(v)
        adj[v].add(u)
    return dict(adj)


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


# TODO: Modify this to use a comprehension.
def sorted_setoset(unsorted: set[frozenset]) -> list[list]:
    """Convert a family of (frozen)sets into a nested list."""
    unsorted_list = []
    for collection in unsorted:
        unsorted_list.append(sorted(collection))  # noqa: PERF401
    return sorted(unsorted_list)


def components(edges: list[tuple[str,str]]) -> set[frozenset[str]]:
    """
    Identify the connected components from an edge list.

    >>> components([])
    set()
    >>> edges = [('1','2'), ('1','3'), ('4','5'),
    ...          ('5','6'), ('3','7'), ('2','7')]
    >>> sorted_setoset(components(edges))
    [['1', '2', '3', '7'], ['4', '5', '6']]
    """
    comp_list = []
    for a, b in edges:
        found = None
        for n, component in enumerate(comp_list):
            if a in component and b not in component:
                component.add(b)
                if found is None:
                    found = n
                else:
                    comp_list[found] |= component
                    del comp_list[n]
                    break
            elif a not in component and b in component:
                component.add(a)
                if found is None:
                    found = n
                else:
                    comp_list[found] |= component
                    del comp_list[n]
                    break
            elif a in component and b in component:
                found = n
                break
        if found is None:
            comp_list.append({a,b})
    comp_set = set()
    for component in comp_list:
        comp_set.add(frozenset(component))
    return comp_set


def components_d(
    edges: list[tuple[str,str]],
    vertices: Iterable[str] = (),
) -> set[frozenset[str]]:
    """
    Identify the connected components from an edge list.

    >>> components_d([])
    set()
    >>> edges = [('1','2'), ('1','3'), ('4','5'),
    ...          ('5','6'), ('3','7'), ('2','7')]
    >>> sorted_setoset(components_d(edges))
    [['1', '2', '3', '7'], ['4', '5', '6']]
    """
    return _setofsets(components_dict(edges, vertices))


def _setofsets(set_dict: dict[object,Iterable]) -> set:
    vals = set()
    for val in distinct(set_dict.values(), key=id):
        vals.add(frozenset(val))
    return vals


def _setofsets_alt(set_dict: dict[object,Iterable]) -> set:
    list_of_sets = distinct(set_dict.values(), key=id)
    return set(map(frozenset, list_of_sets))


def components_dict(
    edges: list[tuple[str,str]],
    vertices: Iterable[str] = (),
) -> dict[str,list[str]]:
    """
    Identify the connected components from an edge list.

    Approximately uses the quick-find algorithm.

    >>> components_dict([])
    {}
    >>> edges = [('1','2'), ('1','3'), ('4','5'),
    ...          ('5','6'), ('3','7'), ('2','7')]
    >>> sorted_setoset(_setofsets(components_dict(edges)))
    [['1', '2', '3', '7'], ['4', '5', '6']]
    """
    comp_dict = {}
    for source, dest in edges:
        if source in comp_dict and dest in comp_dict:
            if comp_dict[source] is not comp_dict[dest]:
                (small,big) = (
                    (source,dest)
                    if len(comp_dict[source]) < len(comp_dict[dest])
                    else (dest,source)
                )
                comp_dict[big] += comp_dict[small]
                for elm in comp_dict[small]:
                    comp_dict[elm] = comp_dict[big]
        elif source in comp_dict:
            comp_dict[source].append(dest)
        elif dest in comp_dict:
            comp_dict[dest].append(source)
        else:
            comp_dict[source] = [source,dest]
            comp_dict[dest] = comp_dict[source]
    for vertex in vertices:
        if vertex not in comp_dict:
            comp_dict[vertex] = [vertex]
    return comp_dict


def components_dict_alt(
    edges: list[tuple[str,str]],
    vertices: Iterable[str] = (),
) -> dict[str,list[str]]:
    """
    Identify the connected components from an edge list.

    uses the quick-find algorithm.

    O(m log(n))
    m = #edges
    n = #vertices

    >>> components_dict_alt([])
    {}
    >>> edges = [('1','2'), ('1','3'), ('4','5'),
    ...          ('5','6'), ('3','7'), ('2','7')]
    >>> sorted_setoset(_setofsets(components_dict_alt(edges)))
    [['1', '2', '3', '7'], ['4', '5', '6']]
    """
    comp_dict = {}
    for source, dest in edges:
        comp_dict[source] = [source]
        comp_dict[dest] = [dest]
    for vertex in vertices:
        comp_dict[vertex] = [vertex]

    for source, dest in edges:
        if comp_dict[source] is not comp_dict[dest]:
            (small,big) = (
                (source,dest)
                if len(comp_dict[source]) < len(comp_dict[dest])
                else (dest,source)
            )
            comp_dict[big] += comp_dict[small]
            for elm in comp_dict[small]:
                comp_dict[elm] = comp_dict[big]
    return comp_dict


# NOTE: components_dict_alt() sort of covers this. So this might be removed.
def components_quickfind(edges: list[tuple[str,str]]) -> set[frozenset[str]]:
    """
    Identify the connected components from an edge list.

    >>> components_quickfind([])
    set()
    >>> edges = [('1','2'), ('1','3'), ('4','5'),
    ...          ('5','6'), ('3','7'), ('2','7')]
    >>> sorted_setoset(components_quickfind(edges))
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


# FIXME: Actually implement classic quick-find.
def components_dict_alt2(
    edges: list[tuple[str,str]],
    vertices: Iterable[str] = (),
) -> dict[str,list[str]]:
    """
    Identify the connected components from an edge list.

    Uses the classic quick-find algorithm.

    >>> components_dict_alt2([])
    {}
    >>> edges = [('1','2'), ('1','3'), ('4','5'),
    ...          ('5','6'), ('3','7'), ('2','7')]
    >>> sorted_setoset(_setofsets(components_dict_alt2(edges)))
    [['1', '2', '3', '7'], ['4', '5', '6']]
    """
    comp_dict = {}
    for source, dest in edges:
        comp_dict[source] = [source]
        comp_dict[dest] = [dest]
    for vertex in vertices:
        comp_dict[vertex] = [vertex]

    for source, dest in edges:
        if comp_dict[source][0] != comp_dict[dest][0]:
            (small,big) = (
                (source,dest)
                if len(comp_dict[source]) < len(comp_dict[dest])
                else (dest,source)
            )
            comp_dict[big] += comp_dict[small]
            for elm in comp_dict[small]:
                comp_dict[elm] = comp_dict[big]
    return comp_dict


# NOTE: components_dict_alt2() may soon cover this. Then this might be removed.
def components_quickfind_classic(
    edges: list[tuple[str,str]],
) -> set[frozenset[str]]:
    """
    Identify the connected components from an edge list.

    This uses classic quick-find (with representative elements), in contrast to
    components(), which is also quick-find but uses list references themselves.

    >>> components_quickfind_classic([])
    set()
    >>> edges = [('1','2'), ('1','3'), ('4','5'),
    ...          ('5','6'), ('3','7'), ('2','7')]
    >>> sorted_setoset(components_quickfind_classic(edges))
    [['1', '2', '3', '7'], ['4', '5', '6']]
    """
    # Make singleton sets.
    representatives = {vertex: vertex for edge in edges for vertex in edge}
    chains = {vertex: [vertex] for vertex in representatives}

    def join_to(to_vertex: str, from_vertex: str) -> None:
        for vertex in chains[from_vertex]:
            representatives[vertex] = to_vertex
        chains[to_vertex].extend(chains[from_vertex])

    def union(u: str, v: str) -> None:
        # Find the parents, stopping if they are already the same.
        u = representatives[u]
        v = representatives[v]
        if u == v:
            return

        # Unite components by size, melding smaller into larger.
        if len(chains[u]) < len(chains[v]):
            join_to(v, u)
        else:
            join_to(u, v)

    for u, v in edges:
        union(u, v)

    canonical_vertices = set(representatives.values())
    return {frozenset(chains[vertex]) for vertex in canonical_vertices}


# NOTE: This may be "reset" into an exercise, or replaced with a completed one.
def components_quickunion(edges: list[tuple[str,str]]) -> set[frozenset[str]]:
    """
    Identify the connected components from an edge list.

    This uses union by rank with path compression.

    >>> components_quickunion([])
    set()
    >>> edges = [('1','2'), ('1','3'), ('4','5'),
    ...          ('5','6'), ('3','7'), ('2','7')]
    >>> sorted_setoset(components_quickunion(edges))
    [['1', '2', '3', '7'], ['4', '5', '6']]
    """
    # Make singleton sets.
    parents = {vertex: vertex for edge in edges for vertex in edge}
    ranks = {vertex: 0 for vertex in parents}

    def find(elem: str) -> str:
        if elem != parents[elem]:
            parents[elem] = find(parents[elem])
        return parents[elem]

    def union(u: str, v: str) -> str:
        # Find the ancestors, stopping if they are already the same.
        u = find(u)
        v = find(v)
        if u == v:
            return

        # Unite the trees by rank.
        if ranks[u] < ranks[v]:
            parents[u] = v
        else:
            if ranks[u] == ranks[v]:
                ranks[u] += 1
            parents[v] = u

    for u, v in edges:
        union(u, v)

    sets_by_ancestor = collections.defaultdict(list)
    for vertex in parents:
        sets_by_ancestor[find(vertex)].append(vertex)
    return {frozenset(component) for component in sets_by_ancestor.values()}


def components_dfs(
    edges: list[tuple[str,str]],
    vertices: Iterable[str] = (),
) -> set[frozenset[str]]:
    """
    Identify the connected components from an edge list.

    That thing where the paths are traversed and the entire component is found,
    then move to the next component.

    >>> components_dfs([])
    set()
    >>> edges = [('1','2'), ('1','3'), ('4','5'),
    ...          ('5','6'), ('3','7'), ('2','7')]
    >>> sorted_setoset(components_dfs(edges))
    [['1', '2', '3', '7'], ['4', '5', '6']]
    """
    adj_list = adjacency(edges, vertices, directed=False)
    comp_set = set()
    visited = set()

    def explore(source, action):
        visited.add(source)
        action(source)
        for dest in adj_list[source]:
            if dest not in visited:
                explore(dest, action)

    for source in adj_list:
        if source not in visited:
            component = []
            explore(source, component.append)
            comp_set.add(frozenset(component))

    return comp_set


# NOTE: components_dfs() covers this. So this might be removed.
def components_dfs_rec(edges: list[tuple[str,str]]) -> set[frozenset[str]]:
    """
    Identify the connected components from an edge list, by recursive DFS.

    This traverses the graph using recursively implemented depth-first search,
    from all vertices.

    >>> components_dfs_rec([])
    set()
    >>> edges = [('1','2'), ('1','3'), ('4','5'),
    ...          ('5','6'), ('3','7'), ('2','7')]
    >>> sorted_setoset(components_dfs_rec(edges))
    [['1', '2', '3', '7'], ['4', '5', '6']]
    """
    adj = adjacency_undirected(edges)
    visited = set()
    all_components = []

    def dfs(src: str, func: Callable[[str], None]) -> None:
        if src in visited:
            return
        visited.add(src)
        func(src)
        for dest in adj[src]:
            dfs(dest, func)

    for start in adj:
        if start in visited:
            continue
        all_components.append([])
        dfs(start, all_components[-1].append)

    return {frozenset(component) for component in all_components}


def devious() -> list[tuple[str,str]]:
    """
    Create a list of edges that defeats components_dfs.

    >>> components_dfs(devious())
    Traceback (most recent call last):
      ...
    RecursionError: maximum recursion depth exceeded

    >>> components_dfs_rec(devious())
    Traceback (most recent call last):
      ...
    RecursionError: maximum recursion depth exceeded
    """
    edges = []
    labels = range(1337)
    for index in labels:
        edges.append((str(index),str(index+1)))  # noqa: PERF401
    return edges


# FIXME: Finish implementing this.
def components_dfs_iter(
    edges: list[tuple[str,str]],
    vertices: Iterable[str] = (),
) -> set[frozenset[str]]:
    """
    Identify the connected components from an edge list.

    This is like components_dfs(), but it tolerates even graphs that would
    cause it to fail with RecursionError (i.e., graphs with long chains).

    >>> components_dfs_iter([])
    set()
    >>> edges = [('1','2'), ('1','3'), ('4','5'),
    ...          ('5','6'), ('3','7'), ('2','7')]
    >>> sorted_setoset(components_dfs_iter(edges))
    [['1', '2', '3', '7'], ['4', '5', '6']]
    """
    adj_list = adjacency(edges, vertices, directed=False)
    comp_set = set()
    visited = set()

    def explore(source, action):
        visited.add(source)
        action(source)
        itst = [iter(adj_list[source])]

    for source in adj_list:
        if source not in visited:
            component = []
            explore(source, component.append)
            comp_set.add(frozenset(component))

    return comp_set


# NOTE: This may be "reset" into an exercise, or replaced with a completed one.
def components_stack(edges: list[tuple[str,str]]) -> set[frozenset[str]]:
    """
    Identify the connected components from an edge list, by stack-based search.

    This traverses the graph using stack-based search, from all vertices. It is
    a naturally iterative algorithm that is somewhat similar to, but not the
    same as, iterative DFS. See:

    https://11011110.github.io/blog/2013/12/17/stack-based-graph-traversal.html

    >>> components_stack([])
    set()
    >>> edges = [('1','2'), ('1','3'), ('4','5'),
    ...          ('5','6'), ('3','7'), ('2','7')]
    >>> sorted_setoset(components_stack(edges))
    [['1', '2', '3', '7'], ['4', '5', '6']]
    """
    adj = adjacency_undirected(edges)
    visited = set()
    all_components = []

    def stack_search(src: str, func: Callable[[str], None]) -> None:
        visited.add(src)
        stack = [src]

        while stack:
            src = stack.pop()
            func(src)
            for dest in adj[src]:
                if dest in visited:
                    continue
                visited.add(dest)
                stack.append(dest)

    for start in adj:
        if start in visited:
            continue
        all_components.append([])
        stack_search(start, all_components[-1].append)

    return {frozenset(component) for component in all_components}


# NOTE: This may be "reset" into an exercise, or replaced with a completed one.
def components_bfs(edges: list[tuple[str,str]]) -> set[frozenset[str]]:
    """
    Identify the connected components from an edge list, by BFS.

    This traverses the graph using breadth-first search, from all vertices.

    >>> components_bfs([])
    set()
    >>> edges = [('1','2'), ('1','3'), ('4','5'),
    ...          ('5','6'), ('3','7'), ('2','7')]
    >>> sorted_setoset(components_bfs(edges))
    [['1', '2', '3', '7'], ['4', '5', '6']]
    """
    adj = adjacency_undirected(edges)
    visited = set()
    all_components = []

    def bfs(src: str, func: Callable[[str], None]) -> None:
        visited.add(src)
        queue = collections.deque((src,))

        while queue:
            src = queue.popleft()
            func(src)
            for dest in adj[src]:
                if dest in visited:
                    continue
                visited.add(dest)
                queue.append(dest)

    for start in adj:
        if start in visited:
            continue
        all_components.append([])
        bfs(start, all_components[-1].append)

    return {frozenset(component) for component in all_components}
