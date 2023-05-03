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
            'conturret': 1,
            'conbot': 1,
            't2conbot': 0,
            'fus': 0,
            'afus': 0,
            'e_store': 1,
            'm_store': 1,
            'conv': 2,
            't2conv': 0,

            # and multiples
            # '8*turbine': 0,
            # '4*conv': 0,
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

    starting_state = setup_utils.TeamState(
        entities=starting_entities,
        metal = 1000.0,
        energy = 1000.0
    )

    desired_entities = ['conbot']

    pareto_optimal_solutions = optimization.multi_objective_search(starting_state=starting_state,
                                                                   desired_entities=desired_entities,
                                                                   build_options=build_options)

    print(pareto_optimal_solutions)

if __name__ == "__main__":
    with cProfile.Profile() as pr:
        main()
    pr.print_stats(sort='cumtime')