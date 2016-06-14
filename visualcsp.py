from csp import *
from collections import defaultdict
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib

class VisualCSP(CSP):

    def __init__(self, vars, domains, neighbors, constraints):
        super(VisualCSP, self).__init__(vars, domains, neighbors, constraints)
        self.assignment_history = []

    def assign(self, var, val, assignment):
        super(VisualCSP, self).assign(var, val, assignment)
        self.assignment_history.append(copy.deepcopy(assignment))

    def unassign(self, var, assignment):
        super(VisualCSP, self).unassign(var, assignment)
        self.assignment_history.append(copy.deepcopy(assignment))

def make_visual(csp):
    return VisualCSP(csp.vars, csp.domains, csp.neighbors,
                     csp.constraints)

def make_update_step_function(graph, visual_csp):

    def draw_graph(graph):
        g = nx.Graph(graph)
        pos = nx.spring_layout(g, k=0.15)
        return (g, pos)
    
    g, pos = draw_graph(graph)

    def update_step(iteration):
        current = visual_csp.assignment_history[iteration]
        current = defaultdict(lambda: 'Black', current)

        colors = [current[n] for n in g.node.keys()]
        nx.draw(g, pos, node_color=colors, node_size=500)
        
        labels = {label:label for label in g.node}
        label_pos = {key:[value[0], value[1]+0.03] for key, value in pos.items()}
        nx.draw_networkx_labels(g, label_pos, labels, font_size=20)

        plt.show()

    return update_step


if __name__ == "__main__":
    vcoloring_problem = make_visual(australia)
    result = backtracking_search(vcoloring_problem)
    step_func = make_update_step_function(australia.neighbors,
                                          vcoloring_problem)

    for i in range(len(vcoloring_problem.assignment_history) ):
        step_func(i)
