from dataclasses import dataclass, field, replace
from TeamState import *
from Entity import *

def fill_build_lists(entities):
    for ent_str, ent in entities.items():
        for build_str, _ in ent.build_list.items():
            ent.build_list[build_str] = entities[build_str]

def load_entities():
    entities = {}

    entities['commander_wreck'] = Entity(
        id_string = 'commander_wreck',
        is_building = False,
        reclaim_value = 2000.0,
        # is_complete = True
    )

    entities['mex'] = Entity(
        id_string = 'mex',
        is_building = True,
        work_required = 1800.0,
        cost_metal = 50.0,
        cost_energy = 500.0,
        metal_production = 2.6, # TODO probably should update this to multiply the map average or somehow get the value passed in
        energy_production = -3.0,
        metal_storage = 50.0,
        reclaim_value = 50.0
    )

    entities['turbine'] = Entity(
        id_string = 'turbine',
        is_building = True,
        work_required = 1603,
        cost_metal = 37.0,
        cost_energy = 175.0,
        energy_production = 10, # TODO see above, same issue
        energy_storage = 0.5,
        reclaim_value = 37.0
    )

    entities['conbot'] = Entity(
        id_string = 'conbot',
        is_building = False,
        is_builder = True,
        build_list = {
            't2botlab': None,
            'turbine': None,
            'mex': None,
            'botlab': None,
            'conturret': None
        },
        work_required=3453,
        cost_energy=1600,
        cost_metal=110,
        build_power=80,
        energy_storage=50,
        reclaim_value=110
    )

    entities['conturret'] = Entity(
        id_string = 'conturret',
        is_building = True,
        is_builder = True,
        build_list = {},
        build_power=200,
        cost_energy=3200,
        cost_metal=210,
        reclaim_value=210,
        work_required=5312
    )

    entities['botlab'] = Entity(
        id_string = 'botlab',
        is_building = True,
        is_builder = True,
        build_list = {
            'conbot': None
        },
        work_required = 6500,
        cost_metal = 650,
        cost_energy = 1200,
        reclaim_value = 650,
        build_power = 100,
        metal_storage = 100,
        energy_storage = 100
    )

    entities['t2conbot'] = Entity(
        id_string = 't2conbot',
        is_building = False,
        is_builder = True,
        build_list = {
            't2botlab': None,
        },
        work_required = 9500,
        cost_metal = 430,
        cost_energy = 6900,
        reclaim_value = 430,
        build_power = 180,
        energy_storage = 100
    )

    entities['t2botlab'] = Entity(
        id_string = 't2botlab',
        is_building = True,
        is_builder = True,
        build_list = {
            't2conbot': None,
        },
        work_required = 75000,
        cost_metal = 2900,
        cost_energy = 15000,
        reclaim_value = 2900,
        build_power = 300,
        metal_storage = 200,
        energy_storage = 200
    )

    entities['commander'] = Entity(
        id_string = 'commander',
        is_building = False,
        is_builder = True,
        build_list = {
            'mex': None,
            'turbine': None,
            # 'commander_wreck': None,
            'botlab': None
        },
        work_required = 75000.0,
        cost_metal = 2700.0,
        cost_energy = 26000.0,
        build_power = 300.0,
        metal_production = 2.0,
        energy_production = 25.0,
        metal_storage = 500.0,
        energy_storage = 500.0,
        is_reclaimable = False,
        # is_complete = True
    )

    fill_build_lists(entities)

    return entities