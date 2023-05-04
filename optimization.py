from typing import List
from dataclasses import dataclass, field
from itertools import count
from Entity import Entity
from Cost import Cost
from TeamState import TeamState
import logging
log = logging.getLogger("deez")

@dataclass
class Node:
    # id: int = field(default_factory=count().__next__, init=False)
    parent_node: 'Node'
    cost: Cost
    state: TeamState

    def __repr__(self):
        return f'NODE {self.cost} {self.state.entities}'

    def generate_neibours(self, build_options):
        neighbour_states = self.state.generate_neighbours(build_options)

        new_nodes = []

        for n in neighbour_states:
            new_nodes.append(Node(parent_node=self,
                             cost=Cost.from_state(n),
                             state=n))
            
        return new_nodes
    
    def is_dominated_by(self: 'Node', y: 'Node'):
        return self.cost.is_dominated_by(y.cost)
    
def update_dominion(n: Node, arr: List[Node]):
    #remove nodes in arr that are dominated by n
    return [x for x in arr if not x.is_dominated_by(n)]

def is_dominated_by_any(x: Node, arr: List[Node]):
    for y in arr:
        if x.is_dominated_by(y):
            log.debug(f'x: {x}, was dominated by {y}')
            return True
    return False

def multi_objective_search(starting_state: TeamState, desired_entities: List[Entity], build_options: dict):

    starting_node = Node(state=starting_state,
                         cost=Cost.from_state(starting_state),
                         parent_node=None)

    open_set = [starting_node]
    solutions = []

    while len(open_set) > 0:

        log.debug(f' len open: {len(open_set)} len sol: {len(solutions)}')

        x = open_set.pop(0) # or from a heuristic or prio q or whatever
        log.debug(f'x: {x}')
        log.debug(f'sols: {solutions}')

        if is_dominated_by_any(x, solutions):
            continue

        if x.state.is_goal(desired_entities):
            log.debug(f'oldsols {solutions}')
            solutions = update_dominion(x, solutions)
            solutions.append(x)
            log.debug(f'newsols {solutions}')
            continue

        successors = x.generate_neibours(build_options)

        for s in successors:
            if is_dominated_by_any(s, solutions):
                continue
            open_set.append(s)

    return solutions