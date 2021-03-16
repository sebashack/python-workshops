import numpy as np
import networkx as nx
import matplotlib.pyplot as plt


def make_map(dim, edges):
    return edges_to_matrix(dim, edges)


def edges_to_matrix(dim, edges):
    mx = np.zeros((dim, dim))

    for (v1, v2) in edges:
        assert v1 != v2
        assert v1 >= 0 and v1 < dim
        assert v2 >= 0 and v2 < dim

        mx[v1][v2] = 1
        mx[v2][v1] = 1

    return mx


def get_num_vertices(graph):
    return graph.shape[0]


def is_safe(graph, v, solution, c):
    for i in range(v):

        if graph[v][i] == 1 and solution[i] == c:
            return False

    return True


def graph_coloring(graph, current_v, solution, colors):
    vertices = get_num_vertices(graph)
    if current_v == vertices:
        return True

    for c in colors:
        if is_safe(graph, current_v, solution, c):

            solution[current_v] = c

            if graph_coloring(graph, current_v + 1, solution, colors):
                return True
            solution[current_v] = 0

    return False


def map_coloring(graph, num_colors):
    solution = np.array([0] * get_num_vertices(graph))
    has_solution = graph_coloring(graph, 0, solution, range(1, num_colors + 1))

    if has_solution:
        return solution
    else:
        return None


def plot_map(graph, solution, node_to_name=None):
    color_map = []
    edges = []
    name_to_node = None

    for (v1, vertex) in enumerate(graph):
        G = nx.Graph()

        for (v2, is_edge) in enumerate(vertex):
            if is_edge == 1 and v1 != v2:
                if node_to_name is not None:
                    edges.append((node_to_name[v1], node_to_name[v2]))
                else:
                    edges.append((v1, v2))

    G.add_edges_from(edges, node_color=color_map)

    if node_to_name is None:
        for node in G:
            color = color_labels[solution[node] - 1]
            color_map.append(color)
    else:
        name_to_node = dict(zip(node_to_name.values(), node_to_name.keys()))
        for node in G:
            color = color_labels[solution[name_to_node[node]] - 1]
            color_map.append(color)

    nx.draw_networkx(
        G, node_color=color_map, with_labels=True, font_size="12", font_weight="bold"
    )

    plt.show()


south_america = {
    0: "colombia",
    1: "venezuela",
    2: "ecuador",
    3: "brazil",
    4: "bolivia",
    5: "peru",
    6: "paraguay",
    7: "uruguay",
    8: "chile",
    9: "argentina",
    10: "guyana",
    11: "suriname",
    12: "guyana-francesa",
}

south_america_edges = [
    (0, 1),
    (0, 2),
    (0, 3),
    (0, 5),
    (1, 3),
    (1, 10),
    (2, 5),
    (3, 4),
    (3, 5),
    (3, 6),
    (3, 7),
    (3, 9),
    (3, 10),
    (3, 11),
    (3, 12),
    (4, 5),
    (4, 6),
    (4, 8),
    (4, 9),
    (5, 8),
    (6, 9),
    (7, 9),
    (8, 9),
]

south_american_map = make_map(13, south_america_edges)

color_labels = ["red", "cyan", "green", "yellow", "blue", "orange", "magenta", "purple"]
