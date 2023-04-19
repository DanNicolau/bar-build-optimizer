#!/bin/python
import setup_utils
import actions
from pprint import pprint

entity_library = setup_utils.load_entities()

print('The entities are:')
print(entity_library.keys())

starting_entities = [
    entity_library['commander']
]



starting_state = setup_utils.TeamState(
    entities=starting_entities,
    metal = 0.0,
    energy = 0.0
)

pprint(starting_state)

desired_entities = ['mex']

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
        print(f'length INSIDE: {len(search_space)}')
    
    search_space = new_states

    print(f'length OUTSIDE: {(search_space)}')

    done = True
