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
        metal_production = 1.8, # TODO probably should update this to multiply the map average or somehow get the value passed in
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
            'conturret': None,
            'e_store': None,
            'm_store': None,
            'conv': None,
        },
        work_required=3453,
        cost_energy=1600,
        cost_metal=110,
        build_power=80,
        energy_storage=50,
        reclaim_value=110,
    )

    entities['conturret'] = Entity(
        id_string = 'conturret',
        is_building = False, #can only help build
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
            'nuke': None,
            't2mex': None,
            'fus': None,
            't2conv': None
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
            'botlab': None,
            'e_store': None,
            'm_store': None,
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

    entities['e_store'] = Entity(
        id_string = 'e_store',
        is_building = True,
        is_builder = False,
        build_list = {},
        work_required = 4119,
        cost_metal = 170,
        cost_energy = 1700,
        energy_storage = 6000
    )

    entities['m_store'] = Entity(
        id_string = 'm_store',
        is_building = True,
        is_builder = False,
        build_list = {},
        work_required = 2925,
        cost_metal = 330,
        cost_energy = 570,
        metal_storage = 3000
    )

    entities['nuke'] = Entity(
        id_string = 'nuke',
        is_building = True,
        is_builder = False,
        build_list = {},
        work_required = 178453.0,
        cost_metal = 8100,
        cost_energy = 90000,
        metal_production = -8.3,
        energy_production = -1042
    )

    #we just record the delta for the t2mex from the t1 mex including the reclaim to simplify calculations
    entities['t2mex'] = Entity(
        id_string = 't2mex',
        is_building = True,
        is_builder = False,
        work_required = 14938 + entities['mex'].work_required, # or not including reclaim cost? idk how this works it looks like it just deletes the t1
        cost_metal = 620 - entities['mex'].cost_metal,
        cost_energy = 7700,
        metal_production = (4.15 - 1) * entities['mex'].metal_production,
        metal_storage = 600,
        energy_production = -20.0
    )

    entities['fus'] = Entity(
        id_string = 'fus',
        is_building = True,
        is_builder = False,
        work_required=70014,
        cost_metal=4300,
        cost_energy=21000,
        energy_production=21000,
        energy_storage=2500
    )

    entities['afus'] = Entity(
        id_string='afus',
        is_building=True,
        is_builder=False,
        work_required=312498,
        cost_metal=9700,
        cost_energy=69000,
        energy_storage=9000,
        energy_production=3000
    )

    entities['conv'] = Entity(
        id_string='conv',
        is_building=True,
        is_builder=False,
        work_required=2605,
        cost_metal=1,
        cost_energy=1150,
        metal_production=1,
        energy_production=-70
    )

    entities['t2conv'] = Entity(
        id_string='t2conv',
        is_building=True,
        is_builder=False,
        work_required=34980,
        cost_metal=380,
        cost_energy=21000,
        metal_production=10,
        energy_production=-600
    )

    fill_build_lists(entities)

    return entities