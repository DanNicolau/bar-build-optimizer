from Solution import Solution
from typing import Dict
from SimpleState import SimpleState
from Entity import Entity

def sim_build(ent: Entity, state: SimpleState, build_options: Dict):
    lib = build_options['entity_library']

    time_to_generate_resources = state.time_to_generate_resources(ent, build_options)

    print(cost)

    exit()

def apply_action(state: SimpleState, action: str, build_options: Dict):

    action_type, action_entity = action.split(':')
    action_entity = build_options['entity_library'][action_entity]

    if action_type == 'build':
        # we assume that this is legal based on the code in vary.py ; 
        # it should not be possible to build something unbuildable here, aside from infinite resource requirements

        sim_build(action_entity, state, build_options)

        raise NotImplementedError()
    elif action_type == 'reclaim':
        raise NotImplementedError()
    elif action_type == 'selfd':
        raise NotImplementedError()
    else:
        raise ValueError("Unknown action type")

    print(action_type, action_entity)
    raise NotImplementedError()

#doesnt have to return anything, just update the score
def evaluate(solution: Solution, build_options: Dict):

    time_to_execute = 0.0

    bo = solution.build_order
    starting_ents = bo.starting_entities
    action_list = bo.action_list
    

    state = SimpleState(entities=starting_ents.copy(),
                        metal=build_options['starting_metal'],
                        energy=build_options['starting_energy'])
    
    print(f'action_list: {action_list}')

    for action in action_list:
        apply_action(state, action, build_options)

    print(state)

    (starting_ents, build_options)

    solution.score = time_to_execute

    raise NotImplementedError()