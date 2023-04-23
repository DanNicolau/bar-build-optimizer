from dataclasses import dataclass, field, replace
from TeamState import *
from Entity import *

def load_entities():
    entities = {}

    entities['commander_wreck'] = Entity(
        id_string = 'commander_wreck',
        is_building = False,
        reclaim_value = 2000.0,
        is_complete = True
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

    entities['commander'] = Entity(
        id_string = 'commander',
        is_building = False,
        is_builder = True,
        build_list = {
            'mex': entities['mex'],
            'turbine': entities['turbine'],
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
        is_complete = True
    )

    return entities