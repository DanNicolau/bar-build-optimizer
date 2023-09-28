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
            'commander': 1,
            'commander_wreck': 1,
            'mex': 3,
            't2mex': 3,
            'geo': 0,
            'botlab': 1,
            't2botlab': 1,
            'turbine': 4,
            'conturret': 8,
            'conbot': 4,
            't2conbot': 1,
            'fus': 1,
            'afus': 1,
            'e_store': 2,
            'm_store': 1,
            'conv': 16,
            't2conv': 2,
            'nuke': 1,

            # and multiples

            # MULTIPLES NOT SUPPORTED FOR SIM ANNEAL

            # '8*turbine': 5,
            # '2*turbine': 2,
            # '4*conv': 2,

            'default_allow': False,
        },
        "time_to_blow_com": 10, # this is probably a bit lower with practice but keeping it around 10 will be ok considering getting the reclaimer to show up
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
    desired_entities = {
        # 'botlab': 1,
        # 'conbot': 2
        'nuke': 1
    }

    print(f'Starting optimization for : {desired_entities}')

    sa.optimize(desired_entities, starting_entities, build_options)





if __name__ == "__main__":
    with cProfile.Profile() as pr:
        main()
    pr.print_stats(sort='tottime')