from dataclasses import dataclass, field, replace
from TeamState import *
from Entity import *

def fill_build_lists(entities):
    for ent_str, ent in entities.items():
        for build_str, _ in ent.build_list.items():
            ent.build_list[build_str] = entities[build_str]

def generate_multiples_lookup(build_restrictions):
    multiples = {}
    for restriction in build_restrictions:
        if '*' in restriction:
            number, id_string = restriction.split('*')
            multiples[id_string] = number
    return multiples

def include_multiples(entity_library, multiples):
    print(f'multiples: {multiples}')

    for multiple, count in multiples.items():
        # print(multiple)
        ent_src = entity_library[multiple]
        ent_new = replace(ent_src)
        ent_new.id_string = f'{count}*{multiple}'
        fcount = float(count)
        ent_new.work_required *= fcount
        ent_new.cost_metal *= fcount
        ent_new.cost_energy *= fcount
        ent_new.build_power *= fcount
        ent_new.energy_production *= fcount
        ent_new.metal_production *= fcount
        ent_new.energy_storage *= fcount
        ent_new.metal_storage *= fcount

        entity_library[ent_new.id_string] = ent_new
        
        for id_string, ent in entity_library.items():
            if multiple in ent.build_list:
                ent.build_list[ent_new.id_string] = ent_new                

def load_entities(options):

    multiples = generate_multiples_lookup(options['build_restrictions'])

    entities = {}

    entities['commander_wreck'] = Entity(
        id_string = 'commander_wreck',
        is_building = False,
        cost_metal = 2000.0,
        work_required = 3600.0, # experimentally determined
        is_reclaimable=True
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
    )

    entities['turbine'] = Entity(
        id_string = 'turbine',
        is_building = True,
        work_required = 1603,
        cost_metal = 37.0,
        cost_energy = 175.0,
        energy_production = 10, # TODO see above, same issue
        energy_storage = 0.5,
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
    )

    entities['conturret'] = Entity(
        id_string = 'conturret',
        is_building = False, #can only help build
        is_builder = True,
        build_list = {},
        build_power=200,
        cost_energy=3200,
        cost_metal=210,
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

    include_multiples(entities, multiples)

    return entities