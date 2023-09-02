#!/bin/python
import setup_utils
import dataclasses
import sys
import cProfile
import multiobjective_optimization
import solutions
import logging
import simulated_annealing
from Cost import Cost

# logging.basicConfig(filename="run.log", level=logging.DEBUG, filemode='w')

def main():
    build_options = {
        # "max_incomplete_buildings": 3, # or should this be equal to the number of workers?.. it should
        # "timestep": 1.0,
        # assume infinite if not defined
        "build_restrictions": {
            'commander_wreck': 1,
            'mex': 5,
            't2mex': 5,
            'geo': 0,
            'botlab': 1,
            't2botlab': 1,
            'turbine': 0,
            'conturret': 3,
            'conbot': 1,
            't2conbot': 0,
            'fus': 0,
            'afus': 0,
            'e_store': 1,
            'm_store': 1,
            'conv': 0,
            't2conv': 0,

            # and multiples

            # MULTIPLES NOT SUPPORTED FOR SIM ANNEAL

            # '8*turbine': 5,
            # '2*turbine': 2,
            # '4*conv': 2,
        },
        "time_to_blow_com": 15,
        "base_metal_storage": 500,
        "base_energy_storage": 500,
        "entity_library": None,
        "built_by": None,
        "prune_stalling": True,
        "starting_metal": 1000,
        "starting_energy": 1000,
        "search_time": 10, # seconds
    }
    build_options['entity_library'], build_options['built_by'] = setup_utils.load_entities(build_options)

    # starting entities
    com = dataclasses.replace(build_options['entity_library']['commander'])
    starting_entities = {
        com.id: com
    }

    desired_entities = ['nuke']

    simulated_annealing.optimize(starting_entities, desired_entities, build_options)




if __name__ == "__main__":
    with cProfile.Profile() as pr:
        main()
    pr.print_stats(sort='cumtime')