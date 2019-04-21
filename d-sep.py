import pprint
pp = pprint.PrettyPrinter(indent=4)

def create_graph():
    """Reads graph.txt and returns a dictionary
    with nodes as keys and the value is a list of
    nodes that the given node has a directed edge to.

    Returns:
        dict: the graph as a dictionary
    """
    with open('graph.txt', 'r') as g_file:
        K = int(g_file.readline())
        graph = {i: [] for i in range(1, K + 1)}
        for line in g_file:
            i, j = map(int, line.split())
            graph[i].append(j)
    return graph


def read_queries():
    """Reads queries.txt and returns a list of X, Y, Z
    triplets.

    Returns:
        list: the list of queries
    """
    with open('queries.txt', 'r') as q_file:
        queries = []
        for line in q_file:
            X, Y, Z = [], [], []
            x, y, z = line.split()
            X.extend(map(int, filter(bool, x[1:-1].split(','))))
            Y.extend(map(int, filter(bool, y[1:-1].split(','))))
            Z.extend(map(int, filter(bool, z[1:-1].split(','))))
            queries.append([X, Y, Z])
    return queries


def is_independent(graph, X, Y, Z):
    """Checks if X is conditionally indepedent
    of Y given Z.

    Args:
        graph (dict): the Bayesian network
        X (list): list of nodes in set X
        Y (list): list of nodes in set Y
        Z (list): list of nodes in set Z

    Returns:
        bool: True if X is conditionally indepedent
    of Y given Z, False otherwise.
    """
    for start in X:
        for end in Y:
            if not is_dsep(graph, start, end, Z):
                return False
    return True


def is_dsep(graph, start, end, obs):
    """Determine d-separation starting from start to end given observed

    Args:
        graph (dict): the Bayesian network
        start (int): start node
        end (int): end node
        observed (list): list of nodes in set Z

    Returns:
        bool
    """
    # 1. We begin by traversing the graph bottom up, from the leaves to the roots,
    # marking all nodes that are in Z or that have descendants in Z.
    obs_anc = get_obs_anc(graph, obs)

    # 2. We traverse breadth-first from X to Y , stopping the traversal along a
    # trail when we get to a blocked node
    via_nodes = [(start, "up")]
    visited = set()
    while len(via_nodes) > 0:
        (node, direction) = via_nodes.pop()

        if (node, direction) not in visited:
            visited.add((node, direction))

            if node not in obs and node == end:
                return False

            if direction == "up" and node not in obs:
                for parent in find_parents(graph, node):
                    via_nodes.append((parent, "up"))
                for child in graph[node]:
                    via_nodes.append((child, "down"))
            elif direction == "down":
                if node not in obs:
                    for child in graph[node]:
                        via_nodes.append((child, "down"))
                if node in obs or node in obs_anc:
                    for parent in find_parents(graph, node):
                        via_nodes.append((parent, "up"))
    return True


def get_obs_anc(graph, observed):
    # copy observed
    visit_nodes = []
    for o in observed:
        visit_nodes.append(o)
    ancestors = set()

    while len(visit_nodes) > 0:
        node = visit_nodes.pop()
        for parent in find_parents(graph, node):
            ancestors.add(parent)
            visit_nodes.append(parent)
    return list(ancestors)


# TODO: parents should be pre-stored
def find_parents(graph, node):
    parents = []
    for key, value in graph.items():
        if node in graph[key]:
            parents.append(key)
    return parents


if __name__ == '__main__':
    graph = create_graph()
    Qs = read_queries()
    for X, Y, Z in Qs:
        output = 1 if is_independent(graph, X, Y, Z) else 0
        print(output)
