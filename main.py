#!/bin/python
import setup_utils
import dataclasses
import sys

def reconstruct_path(path_costs, parents, best_hash):
    print('RECONSTRUCTING')

    path = []

    done = False
    hash_ptr = best_hash
    while hash_ptr != None:
        path.append(f' {hash_ptr}:{path_costs[hash_ptr]}')
        hash_ptr = parents[hash_ptr]

    path.reverse()
    
    return path
    

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

desired_entities = ['conturret']

# the new strat for this will be we have infinite storage, and we spend all the resources at once, then calculate time

build_options = {
    # "max_incomplete_buildings": 3, # or should this be equal to the number of workers?.. it should
    # "timestep": 1.0,
    # "mex_available": 3,
    # "geo_available": 0,
    "build_restrictions": {
        'mex': 3,
        'geo': 0,
        # 'turbine': 40,
        # 'conbot'
    },
    "time_to_blow_com": 15,
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

best_hash = None

min_cost = sys.float_info.max

while len(frontier) > 0:


    v = frontier.pop(0) # default pops last time, change to first for dfs
    v_hash = v.hash()

    # print(f'v: {v}')

    #check if its the goal, if it is then don't find the neighbours
    if (v.is_goal(desired_entities)):
        print(f'popped goal {v}')
        best_hash = v_hash if v.time_elapsed < min_cost else best_hash
        min_cost = min(min_cost, v.time_elapsed)
        continue

    if (v.time_elapsed > min_cost):
        # print(f'time exceeded by: {v}')
        continue


    # add more states to the frontier
    neighbours = v.generate_neighbours(build_options)

    for neighbour in neighbours:
        neighbour_hash = neighbour.hash()
        if (neighbour.time_elapsed >= min_cost):
            continue

        elif (not neighbour_hash in parents):
            # first time we found this hash
            parents[neighbour_hash] = v_hash
            path_costs[neighbour_hash] = neighbour.time_elapsed

            frontier.append(neighbour)
        else:
            # we have found this hash before, if we beat the previous strat replace the parent and cost
            if (path_costs[neighbour_hash] > neighbour.time_elapsed):
                # print('found faster path')
                path_costs[neighbour_hash] = neighbour.time_elapsed
                parents[neighbour_hash] = v_hash

                frontier.append(neighbour)

    print(f'min_cost: {min_cost}, len(frontier): {len(frontier)}, vtime{v.time_elapsed}')


ideal_path = reconstruct_path(path_costs, parents, best_hash)

print(ideal_path)

print('DONE')