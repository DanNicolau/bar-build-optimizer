from typing import List
import TeamState
import Cost
from dataclasses import dataclass, field
from itertools import count
import Entity

def remove_previous_path(costs_arr, parents_arr, cost_to_remove):
    idx = costs_arr.index(cost_to_remove)
    costs_arr.pop(idx)
    parents_arr.pop(idx)

def remove_inferior_goal(goals, goal_to_remove):
    print(f'removing inferior goal: {goal_to_remove}')
    print(f'goals: {goals}')

    goals.remove(goal_to_remove)


def handle_found_goal(new_goal: TeamState, new_goal_cost: Cost, goals: list):
    #if the goal is dominated, return fail
    #if the goal dominates another, excise the other from goals list
    #update global cost limit

    for i in range(len(goals)):
        existing_goal, existing_goal_cost = goals[i]
        if new_goal_cost.is_dominated_by(existing_goal_cost):
            print(f'goal found was inferior')
            return
        elif existing_goal_cost.is_dominated_by(new_goal_cost):
            print(f'goal {new_goal} has beat {existing_goal}')
            remove_inferior_goal(goals, goals[i])

    goals.append((new_goal, new_goal_cost))

@dataclass
class Node:
    id: int = field(default_factory=count().__next__, init=False)
    parent_node: int
    cost: Cost
    state: TeamState

    def generate_neibours(self, build_options):
        neighbour_states = self.state.generate_neighbours(build_options)

        new_nodes = []

        for n in neighbour_states:
            new_nodes.append(Node(parent_node=self.id,
                             cost=Cost.from_state(n),
                             state=n))
            
        return new_nodes
    
    def is_dominated_by(self: 'Node', y: 'Node'):
        return self.cost.is_dominated_by(y.cost)
    
def update_dominion(n: Node, arr: List[Node]):
    #remove nodes in arr that are dominated by n
    arr = [x for x in arr if not x.is_dominated_by(n)]
    return

def is_dominated_by_any(x: Node, arr: List[Node]):
    for y in arr:
        if x.is_dominated_by(y):
            return True
    return False


def multi_objective_search(starting_state, desired_entities, build_options):

    starting_node = Node(state=starting_state,
                         cost=Cost.from_state(starting_state),
                         parent_node=None)

    open_set = [starting_node]
    solutions = []

    while len(open_set) > 0:

        x = open_set.pop(0) # or from a heuristic or prio q or whatever


        print(x)
        exit()

        # if x is dominated by any current solutions:
        #     continue

        # if x is a goal at it to the solutions
        #     ...

        # for each successor of x:
        #     parent (s) in x
        #     cost (s) = cost(x) + difference

        #     if (s) is dominated by any goals
        #         continue
        #     add s to open set

    return solutions