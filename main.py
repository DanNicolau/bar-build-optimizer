#!/bin/python
import setup_utils
import actions

entity_library = setup_utils.load_entities()

print('The entities are:')
print(entity_library.keys())

starting_entities = [
    entity_library['commander']
]

desired_entities = ['mex']

starting_state = setup_utils.TeamState(
    entities=starting_entities,
)

desired_state = setup_utils.TeamState(
    entities=desired_entities,
    available_mex=starting_state.available_mex
)

search_space = [starting_state]


done = False
while not done:
    new_search_space = []
    
    for state in search_space:
        new_states = actions.generate_states(state)
    
    search_space = new_states
