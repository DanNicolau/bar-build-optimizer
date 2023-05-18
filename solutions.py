import sys
from typing import List
from multiobjective_optimization import Node

def get_fastest_solution(solutions: List[Node]):
    min_time = sys.float_info.max
    min_sol = None

    for s in solutions:
        t = s.cost.time_elapsed
        if min_time > t:
            min_time = t
            min_sol = s
    
    if not min_sol:
        raise ValueError("No solutions found")
    return min_sol

def get_path(solution: Node):
    path = []
    while solution:
        path.append(solution)
        solution = solution.parent_node
    path.reverse()
    return path

def get_new_entity(ents_x, ents_y):
    for id in ents_y:
        if not id in ents_x:
            return ents_y[id]


def get_build_order(path_nodes: List[Node]):

    bo = []

    for n, m in zip(path_nodes, path_nodes[1:]):

        ents_x = n.state.entities
        ents_y = m.state.entities

        bo.append((m.cost.time_elapsed, get_new_entity( ents_x, ents_y )))

    return bo