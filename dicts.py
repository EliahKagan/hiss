"""Functions dealing with dictionaries."""

import collections
from collections.abc import Callable

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


# def components_quickfind(edges: list[tuple[str,str]]) -> set[frozenset[str]]:
#     """
#     Identify the connected components from an edge list.
#
#     >>> components_quickfind([])
#     set()
#     >>> edges = [('1','2'), ('1','3'), ('4','5'),
#     ...          ('5','6'), ('3','7'), ('2','7')]
#     >>> sorted_setoset(components_quickfind(edges))
#     [['1', '2', '3', '7'], ['4', '5', '6']]
#     """
#     # Make singleton sets.
#     sets = {vertex: [vertex] for edge in edges for vertex in edge}
#
#     def join(to_set: list[str], from_set: list[str]) -> None:
#         for vertex in from_set:
#             sets[vertex] = to_set
#         to_set.extend(from_set)
#
#     # Unite each edge's endpoints' sets by size, melding smaller into larger.
#     for u, v in edges:
#         u_set = sets[u]
#         v_set = sets[v]
#
#         if u_set is v_set:
#             continue
#
#         if len(u_set) < len(v_set):
#             join(v_set, u_set)
#         else:
#             join(u_set, v_set)
#
#     sets_by_id = {id(component): component for component in sets.values()}
#     return {frozenset(component) for component in sets_by_id.values()}
#
#
# def components_quickfind_classic(
#     edges: list[tuple[str,str]],
# ) -> set[frozenset[str]]:
#     """
#     Identify the connected components from an edge list.
#
#     This uses classic quick-find (with representative elements), in contrast to
#     components(), which is also quick-find but uses list references themselves.
#
#     >>> components_quickfind_classic([])
#     set()
#     >>> edges = [('1','2'), ('1','3'), ('4','5'),
#     ...          ('5','6'), ('3','7'), ('2','7')]
#     >>> sorted_setoset(components_quickfind_classic(edges))
#     [['1', '2', '3', '7'], ['4', '5', '6']]
#     """
#     # Make singleton sets.
#     representatives = {vertex: vertex for edge in edges for vertex in edge}
#     chains = {vertex: [vertex] for vertex in representatives}
#
#     def join(to_vertex: str, from_vertex: str) -> None:
#         for vertex in chains[from_vertex]:
#             representatives[vertex] = to_vertex
#         chains[to_vertex].extend(chains[from_vertex])
#
#     # Unite each edge's endpoints' sets by size, melding smaller into larger.
#     for u, v in edges:
#         u = representatives[u]
#         v = representatives[v]
#
#         if u == v:
#             continue
#
#         if len(chains[u]) < len(chains[v]):
#             join(v, u)
#         else:
#             join(u, v)
#
#     canonical_vertices = set(representatives.values())
#     return {frozenset(chains[vertex]) for vertex in canonical_vertices}
#
#
# def components_quickunion(edges: list[tuple[str,str]]) -> set[frozenset[str]]:
#     """
#     Identify the connected components from an edge list.
#
#     This uses union by rank with path compression.
#
#     >>> components_quickunion([])
#     set()
#     >>> edges = [('1','2'), ('1','3'), ('4','5'),
#     ...          ('5','6'), ('3','7'), ('2','7')]
#     >>> sorted_setoset(components_quickunion(edges))
#     [['1', '2', '3', '7'], ['4', '5', '6']]
#     """
#     # Make singleton sets.
#     parents = {vertex: vertex for edge in edges for vertex in edge}
#     ranks = {vertex: 0 for vertex in parents}
#
#     def find(elem: str) -> str:
#         if elem != parents[elem]:
#             parents[elem] = find(parents[elem])
#         return parents[elem]
#
#     # Unite each edge's endpoints' sets by rank.
#     for u, v in edges:
#         u = find(u)
#         v = find(v)
#
#         if u == v:
#             continue
#
#         if ranks[u] < ranks[v]:
#             parents[u] = v
#         else:
#             if ranks[u] == ranks[v]:
#                 ranks[u] += 1
#             parents[v] = u
#
#     sets_by_ancestor = collections.defaultdict(list)
#     for vertex in parents:
#         sets_by_ancestor[find(vertex)].append(vertex)
#     return {frozenset(component) for component in sets_by_ancestor.values()}
#
#
# def adjacency_undirected(edges: list[tuple[str,str]]) -> dict[str,set[str]]:
#     """
#     Make an adjacency list for an undirected graph.
#
#     >>> adjacency_undirected([])
#     {}
#     >>> adjacency_undirected([('a', 'A')])
#     {'a': {'A'}, 'A': {'a'}}
#     >>> sorted_al(adjacency_undirected([('a','b'), ('b','c'), ('c','a')]))
#     {'a': ['b', 'c'], 'b': ['a', 'c'], 'c': ['a', 'b']}
#     >>> edges = [('a','c'), ('a','b'), ('b','c'), ('c','a')]
#     >>> sorted_al(adjacency_undirected(edges))
#     {'a': ['b', 'c'], 'c': ['a', 'b'], 'b': ['a', 'c']}
#     >>> sorted_al(adjacency_undirected([('a', 'b'), ('c', 'b'), ('d', 'a')]))
#     {'a': ['b', 'd'], 'b': ['a', 'c'], 'c': ['b'], 'd': ['a']}
#     """
#     adj = collections.defaultdict(set)
#     for u, v in edges:
#         adj[u].add(v)
#         adj[v].add(u)
#     return dict(adj)
#
#
# def components_dfs_rec(edges: list[tuple[str,str]]) -> set[frozenset[str]]:
#     """
#     Identify the connected components from an edge list, by recursive DFS.
#
#     This traverses the graph using recursively implemented depth-first search,
#     from all vertices.
#
#     >>> components_dfs_rec([])
#     set()
#     >>> edges = [('1','2'), ('1','3'), ('4','5'),
#     ...          ('5','6'), ('3','7'), ('2','7')]
#     >>> sorted_setoset(components_dfs_rec(edges))
#     [['1', '2', '3', '7'], ['4', '5', '6']]
#     """
#     adj = adjacency_undirected(edges)
#     visited = set()
#     all_components = []
#
#     def dfs(src: str, func: Callable[[str], None]) -> None:
#         if src in visited:
#             return
#         visited.add(src)
#         func(src)
#         for dest in adj[src]:
#             dfs(dest, func)
#
#     for start in adj:
#         if start in visited:
#             continue
#         all_components.append([])
#         dfs(start, all_components[-1].append)
#
#     return {frozenset(component) for component in all_components}
#
#
# def components_stack(edges: list[tuple[str,str]]) -> set[frozenset[str]]:
#     """
#     Identify the connected components from an edge list, by stack-based search.
#
#     This traverses the graph using stack-based search, from all vertices. It is
#     a naturally iterative algorithm that is somewhat similar to, but not the
#     same as, iterative DFS. See:
#
#     https://11011110.github.io/blog/2013/12/17/stack-based-graph-traversal.html
#
#     >>> components_stack([])
#     set()
#     >>> edges = [('1','2'), ('1','3'), ('4','5'),
#     ...          ('5','6'), ('3','7'), ('2','7')]
#     >>> sorted_setoset(components_stack(edges))
#     [['1', '2', '3', '7'], ['4', '5', '6']]
#     """
#     adj = adjacency_undirected(edges)
#     visited = set()
#     all_components = []
#
#     def stack_search(src: str, func: Callable[[str], None]) -> None:
#         visited.add(src)
#         stack = [src]
#
#         while stack:
#             src = stack.pop()
#             func(src)
#             for dest in adj[src]:
#                 if dest in visited:
#                     continue
#                 visited.add(dest)
#                 stack.append(dest)
#
#     for start in adj:
#         if start in visited:
#             continue
#         all_components.append([])
#         stack_search(start, all_components[-1].append)
#
#     return {frozenset(component) for component in all_components}
#
#
# def components_bfs(edges: list[tuple[str,str]]) -> set[frozenset[str]]:
#     """
#     Identify the connected components from an edge list, by BFS.
#
#     This traverses the graph using breadth-first search, from all vertices.
#
#     >>> components_bfs([])
#     set()
#     >>> edges = [('1','2'), ('1','3'), ('4','5'),
#     ...          ('5','6'), ('3','7'), ('2','7')]
#     >>> sorted_setoset(components_bfs(edges))
#     [['1', '2', '3', '7'], ['4', '5', '6']]
#     """
#     adj = adjacency_undirected(edges)
#     visited = set()
#     all_components = []
#
#     def bfs(src: str, func: Callable[[str], None]) -> None:
#         visited.add(src)
#         queue = collections.deque((src,))
#
#         while queue:
#             src = queue.popleft()
#             func(src)
#             for dest in adj[src]:
#                 if dest in visited:
#                     continue
#                 visited.add(dest)
#                 queue.append(dest)
#
#     for start in adj:
#         if start in visited:
#             continue
#         all_components.append([])
#         bfs(start, all_components[-1].append)
#
#     return {frozenset(component) for component in all_components}
