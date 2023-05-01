#!/bin/python
import setup_utils
import dataclasses
import sys
import cProfile
import optimization
from reconstruct_path import *
from Cost import Cost

def main():
    build_options = {
        # "max_incomplete_buildings": 3, # or should this be equal to the number of workers?.. it should
        # "timestep": 1.0,
        "build_restrictions": {
            'commander_wreck': 0,
            'mex': 3,
            't2mex': 3,
            'geo': 0,
            'botlab': 1,
            't2botlab': 0,
            'turbine': 10,
            '8*turbine': 0,
            'conturret': 1,
            'conbot': 1,
            't2conbot': 0,
            'fus': 0,
            'afus': 0,
            'e_store': 1,
            'm_store': 1,
            'conv': 2,
            '4*conv': 0,
            't2conv': 0
        },
        "time_to_blow_com": 15,
        "base_metal_storage": 500,
        "base_energy_storage": 500,
        "entity_library": None
    }

    build_options['entity_library'] = setup_utils.load_entities(build_options)

    com = dataclasses.replace(build_options['entity_library']['commander'])

    starting_entities = {
        com.id: com
    }

    starting_node = setup_utils.TeamState(
        entities=starting_entities,
        metal = 1000.0,
        energy = 1000.0
    )

    desired_entities = ['mex','turbine']

    # the new strat for this will be we have infinite storage, and we spend all the resources at once, then calculate time

    explored_space = []
    frontier = [starting_node]
    unexplored_space = []

    print('STARTING')
    print(starting_node)

    path_costs = {}
    parents = {}
    path_costs[starting_node.hash()] = [Cost.from_state(starting_node)]
    print(path_costs)
    parents[starting_node.hash()] = []

    #solutions that are not dominated by others
    pareto_optimal_solutions = []

    #update this to speed up initial search removing stupid builds once any solution is found, if this is below fastest, no solution returns
    # cost_limit = Cost(-1, sys.float_info.max, 0, 0)
    min_time = sys.float_info.max

    goals = [] #list of (state, cost) pairs

    i = 0

    while len(frontier) > 0:
        i+=1 
        if (i==1000):
            exit()
        print('\n\n')
        print(f'frontier: {frontier}')

        v = frontier.pop(0)
        v_hash = v.hash()
        print(f'popped {v}, then generated neighbours')


        neighbours = v.generate_neighbours(build_options)
        print(f'neighbours: {neighbours}')

        for neighbour in neighbours:
            go_to_next_neighbour = False
            #check neighbour costs
            neighbour_cost = Cost.from_state(neighbour)
            for (goal, goal_cost) in goals:
                if (neighbour_cost.is_dominated_by(goal_cost)):
                    print(f'skipping due to better goal, neighbour {neighbour} \tdom by {goal}')
                    go_to_next_neighbour = True
                    break

            if go_to_next_neighbour:
                continue

            neighbour_hash = neighbour.hash()
            if (neighbour.is_goal(desired_entities)):
                print(f'found goal {neighbour} ... moving on')
                optimization.handle_found_goal(neighbour, neighbour_cost, goals)
                print(f'goals: {goals}')
                continue
            elif (neighbour_hash in path_costs):
                print(f'found previous hash {neighbour_hash}')
                for existing_cost in path_costs[neighbour_hash]:
                    if neighbour_cost.is_dominated_by(existing_cost):
                        break #exi this node's processingt, this neighbors completely worse than another solutions
                    elif existing_cost.is_dominated_by(neighbour_cost):
                        #remove the existing cost and its parents since they are not relevant anymore
                        optimization.remove_previous_path(path_costs[neighbour_hash], parents[neighbour_hash], existing_cost)
                    #if we haven't break'd by now this needs to go on the frontier
                    frontier.append(neighbour)
                    
                # raise NotImplementedError()
            else:
                print(f'found new hash: {neighbour_hash}')
                #was not in the path costs
                path_costs[neighbour_hash] = [neighbour_cost] # sketchy decision to append and remove from these lists in parallel, they must relate to each other!
                parents[neighbour_hash] = [v_hash]
                frontier.append(neighbour)


            print('c_arrs', path_costs)
            print('parents', parents)

            
            

        # v = frontier.pop(0) # default pops last time, change to first for dfs
        # print(f'min_cost: {min_cost:.2f}, len(frontier): {len(frontier)}, vtime{v.time_elapsed:.2f}')

        # v_hash = v.hash()

        # # print(f'v: {v}')

        # #check if its the goal, if it is then don't find the neighbours
        # if (v.is_goal(desired_entities)):
        #     # print(f'popped goal {v}')
        #     best_hash = v_hash if v.time_elapsed < min_cost else best_hash
        #     min_cost = min(min_cost, v.time_elapsed)
        #     continue

        # if (v.time_elapsed > min_cost):
        #     # print(f'time exceeded by: {v}')
        #     continue

        # # add more states to the frontier
        # neighbours = v.generate_neighbours(build_options)

        # for neighbour in neighbours:
        #     neighbour_hash = neighbour.hash()
        #     if (neighbour.time_elapsed >= min_cost):
        #         # print(f'neighbour: {neighbour.time_elapsed}, mincost: {min_cost}')
        #         # print("longer than current solution")
        #         continue

        #     elif (not neighbour_hash in parents):
        #         # first time we found this hash
        #         # print("first find")
        #         parents[neighbour_hash] = v_hash
        #         path_costs[neighbour_hash] = neighbour.time_elapsed

        #         frontier.append(neighbour)
        #     else:
        #         # we have found this hash before, if we beat the previous strat replace the parent and cost
        #         if (path_costs[neighbour_hash] > neighbour.time_elapsed):
        #             # print('found faster path')
        #             path_costs[neighbour_hash] = neighbour.time_elapsed
        #             parents[neighbour_hash] = v_hash

        #             frontier.append(neighbour)
        #         # else:
        #         #     # print("too slow")


    if len(goals) == 0:
        print('No solution found')
        return
    
    print(path_costs)
    print(parents)

    ideal_path = reconstruct_path(path_costs, parents)

    print(ideal_path)

    print_build_order_delta(ideal_path)

if __name__ == "__main__":
    with cProfile.Profile() as pr:
        main()
    pr.print_stats(sort='cumtime')