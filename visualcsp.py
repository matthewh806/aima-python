from csp import *
from collections import defaultdict
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib import lines 

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

class CspPlotter():

    def __init__(self, graph, visual_csp):
        self.graph = graph
        self.visual_csp = visual_csp
        self.min = 0
        self.max = len(self.visual_csp.assignment_history) - 1
        self.cur = 0
        self.g = nx.Graph(self.graph)
        self.pos = nx.spring_layout(self.g, k=0.15)
        self.update()
    
    def update(self):
        current = self.visual_csp.assignment_history[self.cur]
        current = defaultdict(lambda: 'Black', current)

        colors = [current[n] for n in self.g.node.keys()]
        nx.draw(self.g, self.pos, node_color=colors, node_size=500)
        
        labels = {label:label for label in self.g.node}
        label_pos = {key:[value[0], value[1]+0.03] for key, value in self.pos.items()}
        nx.draw_networkx_labels(self.g, label_pos, labels, font_size=20)
        
        plt.draw()

    def on_press(self,event):
        if event.key not in ('left', 'right'):
            return
        if event.key == 'right':
            self.cur += 1
        else:
            self.cur -= 1

        self.cur = max(self.min, min(self.cur, self.max))
        self.update() 


if __name__ == "__main__":
    vcoloring_problem = make_visual(australia)
    result = backtracking_search(vcoloring_problem)
    plotter = CspPlotter(australia.neighbors, vcoloring_problem)

    fig = plt.gcf()
    fig.canvas.mpl_connect('key_press_event', plotter.on_press)
    plt.title('Visual CSP: Australia map coloring',
          horizontalalignment='center')
    black_circle = lines.Line2D([], [], color="Black", marker='o',
                                markersize=15, markerfacecolor="black")
    plt.legend([black_circle], ['Unassigned'], numpoints=1)
    plt.show()
