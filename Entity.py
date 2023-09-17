from dataclasses import dataclass, field, replace
from typing import List, Dict
from itertools import count
from pprint import pprint

@dataclass
class Entity:
    id_string: str
    is_building: bool
    id: int = field(default_factory=count().__next__, init=False)
    is_builder: bool = field(default = False)
    build_list: Dict = field(default_factory = lambda: {})
    work_required: float = field(default = 0.0)
    cost_metal: float = field(default = 0.0) # this might actually speed up if its an int
    cost_energy: float = field(default = 0.0)
    build_power: float = field(default = 0.0)
    energy_production: float = field(default = 0.0)
    metal_production: float = field(default = 0.0)
    energy_storage: float = field(default = 0.0)
    metal_storage: float = field(default = 0.0)
    is_reclaimable: bool = field(default = True)
    is_factory: bool = field(default = False)
    is_reclaimer: bool = field(default = False)
    is_possible_final_constructor: bool = field(default = False)

    def __repr__(self):
        return f'ent{self.id}-{self.id_string} '
    
    def long_print(self):
        pprint(vars(self))