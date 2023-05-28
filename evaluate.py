from Solution import Solution
from typing import Dict
from SimpleState import SimpleState

def handle_action():
    raise NotImplementedError

#doesnt have to return anything, just update the score
def evaluate(solution: Solution, build_options: Dict):

    time_to_execute = 0.0

    bo = solution.build_order
    starting_ents = bo.starting_entities
    action_list = bo.action_list

    state = SimpleState(starting_ents.copy(),
                        build_options['starting_metal'],
                        build_options['starting_energy'])
    
    print(f'action_list: {action_list}')

    for action in action_list:
        handle_action()

    print(state)

    (starting_ents, build_options)

    solution.score = time_to_execute