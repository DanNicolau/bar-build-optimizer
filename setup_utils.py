from dataclasses import dataclass, field
from typing import List

@dataclass
class Entity:
    # id: int
    is_building: bool
    is_builder: bool
    build_list: List['Entity']
    work_required: float
    cost_metal: float  # this might actually speed up if its an int
    cost_energy: float
    build_power: float
    energy_production: float
    metal_production: float

@dataclass
class TeamState:
    required_entities: List[Entity]
    available_mex: int # check mex doesn't exceed this

def load_entities():
    entities = {}

    entities['commander'] = Entity(
        is_building = False,
        is_builder = True,
        build_list = ['mex'],
        work_required = 75000.0,
        cost_metal = 2700.0,
        cost_energy = 26000.0,
        build_power = 300.0,
        metal_production = 2.0,
        energy_production = 25.0,

    )

    entities['mex'] = Entity(
        is_building = True,
        is_builder = False,
        build_list = [],
        work_required = 1800.0,
        cost_metal = 50.0,
        cost_energy = 500.0,
        build_power = 0.0,
        metal_production = 2.6, # TODO probably should update this to multiply the map average or somehow get the value passed in
        energy_production = -3.0,
    )

    entities['turbine'] = Entity(
        is_building = True,
        is_builder = False,
        build_list = [],
        work_required = 1603,
        cost_metal = 37.0,
        cost_energy = 175.0,
        build_power = 0.0,
        metal_production = 0.0,
        energy_production = 10 # TODO see above, same issue
    )

    return entities