class Flowchart :
    def __init__(self, id, name, graph):
        self.id = id
        self.name = name
        self.graph = graph

    def view_graph(self):
        for vertex, nodes in self.graph.items():
            print(f"{vertex} : ", end=" ") 
            for node in nodes:
                print(f"{node} ,", end=" ")
            print("")

def make_nodes(relations: str):
    return ''.join(sorted(set(relations)))

def make_edges(relations: str):
    return [relations[i:i+2] for i in range(0, len(relations)-1, 2)]

def make_graph(nodes: str, relations: list[str]):
    graph = {}
    for node in nodes:
        graph[node] = []
        for relation in relations:
            if relation[0] == node:
                graph[node].append(relation[1])
    return graph

def update_add_edge(self, relations: str):
    edges = make_edges(relations=relations)
    graph = self.graph
    for edge in edges:
        if not graph.get(edge[0]):
            graph[edge[0]] = []
        if edge[1] in graph[edge[0]]:
            continue
        graph[edge[0]].append(edge[1])
    return self.graph

def update_remove_edge(self, relations: str):
    edges = make_edges(relations=relations)
    graph = self.graph
    for edge in edges:
        if not graph.get(edge[0]):
            continue
        if edge[1] in graph[edge[0]]:
            graph[edge[0]].remove(edge[1])
    return self.graph

def fetch_outgoing_edges(self, edge: str) -> int:
    graph = self.graph
    if graph.get(edge) == None:
        return -1
    return len(graph[edge])



def create_flowchart(id: int, name: str, relations: str) -> Flowchart:
    nodes = make_nodes(relations=relations)
    edges = make_edges(relations=relations)
    graph = make_graph(nodes=nodes, relations=edges)

    chart = Flowchart(id=id, name=name, graph=graph)
    return chart
