from _typeshed import Incomplete

from networkx.utils.backends import _dispatchable

@_dispatchable
def fast_gnp_random_graph(n, p, seed: Incomplete | None = None, directed: bool = False): ...
@_dispatchable
def gnp_random_graph(n, p, seed: Incomplete | None = None, directed: bool = False): ...

binomial_graph = gnp_random_graph
erdos_renyi_graph = gnp_random_graph

@_dispatchable
def dense_gnm_random_graph(n, m, seed: Incomplete | None = None): ...
@_dispatchable
def gnm_random_graph(n, m, seed: Incomplete | None = None, directed: bool = False): ...
@_dispatchable
def newman_watts_strogatz_graph(n, k, p, seed: Incomplete | None = None): ...
@_dispatchable
def watts_strogatz_graph(n, k, p, seed: Incomplete | None = None): ...
@_dispatchable
def connected_watts_strogatz_graph(n, k, p, tries: int = 100, seed: Incomplete | None = None): ...
@_dispatchable
def random_regular_graph(d, n, seed: Incomplete | None = None): ...
@_dispatchable
def barabasi_albert_graph(n, m, seed: Incomplete | None = None, initial_graph: Incomplete | None = None): ...
@_dispatchable
def dual_barabasi_albert_graph(n, m1, m2, p, seed: Incomplete | None = None, initial_graph: Incomplete | None = None): ...
@_dispatchable
def extended_barabasi_albert_graph(n, m, p, q, seed: Incomplete | None = None): ...
@_dispatchable
def powerlaw_cluster_graph(n, m, p, seed: Incomplete | None = None): ...
@_dispatchable
def random_lobster(n, p1, p2, seed: Incomplete | None = None): ...
@_dispatchable
def random_shell_graph(constructor, seed: Incomplete | None = None): ...
@_dispatchable
def random_powerlaw_tree(n, gamma: float = 3, seed: Incomplete | None = None, tries: int = 100): ...
@_dispatchable
def random_powerlaw_tree_sequence(n, gamma: float = 3, seed: Incomplete | None = None, tries: int = 100): ...
@_dispatchable
def random_kernel_graph(n, kernel_integral, kernel_root: Incomplete | None = None, seed: Incomplete | None = None): ...
