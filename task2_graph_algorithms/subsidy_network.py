"""
Separate graph just to show off Bellman-Ford's negative weight handling.

Thing is, real road distance can never be negative, so if I tested
Bellman-Ford on the actual Nepal road network it would just behave
exactly like Dijkstra - technically correct but doesn't really show
anything interesting.

So instead this models COST instead of distance. Idea: government
subsidises certain routes to encourage trade to remote regions, so the
"effective cost" of taking that route (toll + fuel - subsidy) can end up
being less than zero if the subsidy is generous enough. Gives us a
legit reason to have negative edges without just making up random
negative numbers.

Also added an option to inject a negative cycle on purpose - a subsidy
loop where the cost just keeps dropping every time you go round it,
which obviously makes no real sense (you could "earn" infinite money by
driving in circles) and is exactly the kind of broken cost model
Bellman-Ford is supposed to catch. Dijkstra would have no way of
detecting this at all.
"""
from graph import Graph


def build_subsidy_graph(with_negative_cycle=False):
    """
    Reusing the same city ids as nepal_network.py so it's still Nepal
    even though the edge weights here mean something totally different
    (relative cost units, not km).
    """
    g = Graph(directed=True)
    edges = [
        (0, 11, 40),    # Kathmandu -> Hetauda: normal toll + fuel cost
        (11, 5, -15),   # Hetauda -> Birgunj: subsidised trade route, net negative
        (5, 10, 20),    # Birgunj -> Janakpur: normal cost
        (10, 4, -10),   # Janakpur -> Biratnagar: subsidised border trade route
        (0, 7, 35),     # Kathmandu -> Bharatpur: normal cost
        (7, 11, -8),    # Bharatpur -> Hetauda: subsidised feeder route
    ]
    for u, v, w in edges:
        g.add_edge(u, v, w)

    if with_negative_cycle:
        # cycle: Hetauda -> Bharatpur -> Hetauda, total weight -13
        # (an over-generous subsidy on both legs) - this is the broken
        # case Bellman-Ford should flag
        g.add_edge(11, 7, -5)   # Hetauda -> Bharatpur (subsidised)
        # (7, 11, -8) already exists above, so cycle = -5 + -8 = -13 < 0

    return g