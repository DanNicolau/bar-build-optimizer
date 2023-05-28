from Solution import Solution
from typing import Dict, List
import random
import copy

def append_to_actions(possible_actions: List, new_action: str):
    if not new_action in possible_actions:
        possible_actions.append(new_action)

def generate_random_action(source_solution: Solution, build_options:Dict):
    possible_actions = []

    # create all possible actions
    entities = source_solution.build_order.starting_entities
    ent_lib = build_options["entity_library"]

    for ent_str in entities:
        ent = ent_lib[ent_str]
        if ent.id_string == 'commander':
            append_to_actions(possible_actions, 'selfd:commander')
        if ent.is_reclaimable:
            append_to_actions(possible_actions, f'reclaim: {ent.id_string}')
        for build_option in ent.build_list:
            append_to_actions(possible_actions, f'build:{build_option}')

    return random.choice(possible_actions)

#varies the solution in a small way, this must return a copy of the input, not a reference to the same object passed in
def vary_solution(source_solution: Solution, build_options: Dict):

    new_solution = copy.deepcopy(source_solution)

    # variations are either adding or removing from the build order at a random index in the build order
    action_list_len = len(new_solution.build_order.action_list)
    if random.randint(0,1) == 0:
        #add
        new_action = generate_random_action(new_solution, build_options)
        index_to_insert = random.randint(0, action_list_len)
        new_solution.build_order.action_list.insert(index_to_insert, new_action)

    elif action_list_len > 0:
        index_to_remove = random.randint(0, action_list_len)
        del new_solution.build_order.action_list[index_to_remove]

    #TODO swap? perhaps this will lead to more precisely optimized builds

    return new_solution