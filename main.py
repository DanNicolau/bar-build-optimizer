#!/bin/python
import setup_utils
import dataclasses
import sys
import cProfile

import simulated_annealing as sa
# logging.basicConfig(filename="run.log", level=logging.DEBUG, filemode='w')

def main():
    build_options = {
        # "max_incomplete_buildings": 3, # or should this be equal to the number of workers?.. it should
        # "timestep": 1.0,
        # assume infinite if not defined
        "build_restrictions": {
            'commander_wreck': 1,
            'mex': 3,
            't2mex': 0,
            'geo': 0,
            'botlab': 1,
            't2botlab': 0,
            'turbine': 4,
            'conturret': 1,
            'conbot': 1,
            't2conbot': 0,
            'fus': 0,
            'afus': 0,
            'e_store': 0,
            'm_store': 0,
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
    starting_entities = ['commander']
    desired_entities = ['botlab']

    print(f'Starting optimization for : {desired_entities}')

    sa.optimize(desired_entities, starting_entities, build_options)





if __name__ == "__main__":
    with cProfile.Profile() as pr:
        main()
    pr.print_stats(sort='cumtime')