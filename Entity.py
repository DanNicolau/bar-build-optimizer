from dataclasses import dataclass, field, replace
from typing import List, Dict
from itertools import count

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
    reclaim_value: float = field(default = 0.0)
    is_complete: bool = field(default = False)
    is_reclaimable: bool = field(default = True)

    def __repr__(self):
        return f'ent{self.id}-{self.id_string} '
    
    def new_building(self, new_id=True):
        old_id = self.id
        new_building = replace(self)
        new_building.is_complete = False
        new_building.work_completed = 0.0

        if not new_id:
            new_building.id = old_id

        return new_building