#!/bin/python
import setup_utils
from actions import generate_states
import dataclasses
from pprint import pprint
from goals import *

entity_library = setup_utils.load_entities()

com = dataclasses.replace(entity_library['commander'])

starting_entities = {
    com.id: com
}

starting_state = setup_utils.TeamState(
    entities=starting_entities,
    parent = -1,
    metal = 1000.0,
    energy = 1000.0
)

desired_entities = ['mex']

# the new strat for this will be we have infinite storage, and we spend all the resources at once

done = False
iterations = 0
explored_space = []
frontier = [starting_state]
unexplored_space = []

build_options = {
    # "max_incomplete_buildings": 3, # or should this be equal to the number of workers?.. it should
    "timestep": 1.0,
    "mex_available": 3,
    "base_metal_storage": 500,
    "base_energy_storage": 500,
    "entity_library": entity_library
}

print('STARTING')
print(starting_state)

while not done:

    n = frontier.pop() # default pops last time, change to first for dfs

    # add more states to the frontier
    frontier.extend(generate_states(n, build_options))

    print(f'FRONTIER: {frontier}')

    explored_space.append(n)

    iterations += 1

    for ent_id, ent in n.entities.items():
        if ent.is_complete and not ent.is_builder:
            done = True

    # done = len(frontier) == 0

print(f'FRONTIER: {frontier}')

print('EXPLORED:')
print(explored_space)