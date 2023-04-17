from dataclasses import dataclass, field
from typing import List
from itertools import count

@dataclass
class Entity:
    id: int = field(default_factory=count().__next__, init=False)
    is_building: bool 
    is_builder: bool = field(default = False)
    build_list: List['Entity'] = field(default_factory = lambda: [])
    work_required: float = field(default = 0.0)
    work_completed: float = field(default = 0.0)
    cost_metal: float = field(default = 0.0) # this might actually speed up if its an int
    cost_energy: float = field(default = 0.0)
    build_power: float = field(default = 0.0)
    energy_production: float = field(default = 0.0)
    metal_production: float = field(default = 0.0)
    energy_storage: float = field(default = 0.0)
    metal_storage: float = field(default = 0.0)
    reclaim_value: float = field(default = 0.0)
    is_complete: bool = field(default = False)

@dataclass
class TeamState:
    id: int = field(default_factory=count().__next__, init=False)
    entities: List[Entity]
    available_mex: int = field(default = 3) # check mex doesn't exceed this
    base_metal_storage: float = field(default = 500.0)
    base_energy_storage: float = field(default = 0.0)
    metal: float = field(default = 0)
    energy: float = field(default = 0)

def load_entities():
    entities = {}

    entities['commander'] = Entity(
        is_building = False,
        is_builder = True,
        build_list = ['mex', 'turbine'],
        work_required = 75000.0,
        cost_metal = 2700.0,
        cost_energy = 26000.0,
        build_power = 300.0,
        metal_production = 2.0,
        energy_production = 25.0,
        metal_storage = 500.0,
        energy_storage = 500.0
    )

    entities['commander_wreck'] = Entity(
        is_building = False,
        reclaim_value = 2000.0
    )

    entities['mex'] = Entity(
        is_building = True,
        work_required = 1800.0,
        cost_metal = 50.0,
        cost_energy = 500.0,
        metal_production = 2.6, # TODO probably should update this to multiply the map average or somehow get the value passed in
        energy_production = -3.0,
        metal_storage = 50.0
    )

    entities['turbine'] = Entity(
        is_building = True,
        work_required = 1603,
        cost_metal = 37.0,
        cost_energy = 175.0,
        energy_production = 10, # TODO see above, same issue
        energy_storage = 0.5
    )

    return entities