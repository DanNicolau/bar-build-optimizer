from Solution import Solution
from typing import Dict, List

def append_to_actions(possible_actions: List, new_action: str):
    if not new_action in possible_actions:
        possible_actions.append(new_action)

#varies the solution in a small way, this must return a copy of the input, not a reference to the same object passed in
def vary_solution(source_solution: Solution, build_options: Dict):

    possible_actions = []

    # create all possible actions
    entities = source_solution.build_order.starting_entities
    ent_lib = build_options["entity_library"]

    print(ent_lib)

    for ent_str in entities:
        ent = ent_lib[ent_str]
        if ent.id_string == 'commander':
            append_to_actions(possible_actions, 'selfdcom')
        if ent.is_reclaimable:
            append_to_actions(possible_actions, f'reclaim: {ent.id_string}')
        for build_option in ent.build_list:
            append_to_actions(possible_actions, f'build:{build_option}')

    # randomly choose one

    # apply action

    # return solution

    raise NotImplementedError()