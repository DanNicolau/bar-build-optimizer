#!/bin/python
import setup_utils
import dataclasses
from pprint import pprint

entity_library = setup_utils.load_entities()

com = dataclasses.replace(entity_library['commander'])

starting_entities = {
    com.id: com
}

starting_node = setup_utils.TeamState(
    entities=starting_entities,
    metal = 1000.0,
    energy = 1000.0
)

desired_entities = ['mex', 'mex']

# the new strat for this will be we have infinite storage, and we spend all the resources at once



build_options = {
    # "max_incomplete_buildings": 3, # or should this be equal to the number of workers?.. it should
    # "timestep": 1.0,
    "mex_available": 3,
    "geo_available": 0,
    # "base_metal_storage": 500,
    # "base_energy_storage": 500,
    "entity_library": entity_library
}

explored_space = []
frontier = [starting_node]
unexplored_space = []

print('STARTING')
print(starting_node)

path_costs = {}
parents = {}
path_costs[starting_node.hash()] = 0
parents[starting_node.hash()] = None

while len(frontier) > 0:


    v = frontier.pop(0) # default pops last time, change to first for dfs

    #check if its the goal, if it is then don't find the neighbours
    if (v.is_goal(desired_entities)):
        continue

    v_hash = v.hash()

    # add more states to the frontier
    neighbours = v.generate_neighbours(build_options)

    for neighbour in neighbours:
        neighbour_hash = neighbour.hash()

        if (not neighbour_hash in parents):
            # first time we found this hash
            parents[neighbour_hash] = v_hash
            path_costs[neighbour_hash] = neighbour.time_elapsed

            frontier.append(neighbour)
        else:
            # we have found this hash before, if we beat the previous strat replace the parent and cost
            if (path_costs[neighbour_hash] > neighbour.time_elapsed):
                print('found faster path')
                path_costs[neighbour_hash] = neighbour.time_elapsed
                parents[neighbour_hash] = v_hash

                frontier.append(neighbour)

    print('COSTS')
    print(path_costs)
    print('PARENTS')
    print(parents)

    print(f'FRONTIER: {frontier}')

    # explored_space.append(v)