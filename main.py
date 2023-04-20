#!/bin/python
import setup_utils
import actions
import dataclasses
from pprint import pprint
from goals import *

entity_library = setup_utils.load_entities()

# print('The entities are:')
# print(entity_library.keys())

starting_entities = [
    dataclasses.replace(entity_library['commander'])
]



starting_state = setup_utils.TeamState(
    entities=starting_entities,
    metal = 0.0,
    energy = 0.0
)

# print(starting_state)

desired_entities = ['mex']*3

# desired_state = setup_utils.TeamState(
#     entities=desired_entities
# )

search_space = [starting_state]
done = False
iterations = 0

while not done:
    
    new_states = []

    for state in search_space:
        new_states.extend(actions.generate_states(state))

        #TODO remove searched elements, but somehow keep a path of how we got there?, DFS

        for ns in new_states:
            print('NEW STATE')
            for ent in ns.entities:
                print(ent.id_string)
    
    #TODO
    # prune(new_staes)
    
    search_space = new_states



    iterations += 1
    
    for state in search_space:
        if (goal_criteria_met(desired_entities, state)):
            print('GOAL MET')
            done = True
            break

    if (iterations == 2):
        print('MAX ITERS MET')
        done = True