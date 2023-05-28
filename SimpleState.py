from dataclasses import dataclass
from Entity import Entity
from typing import List

@dataclass
class SimpleState:
    entities: List[Entity]
    metal: float
    energy: float

    def get_production(self):
        metal_prod = 0.0
        energy_prod = 0.0
        for ent in self.entities:
            metal_prod += ent.metal_production
            energy_prod += ent.energy_production
        return metal_prod, energy_prod

    def get_storage(self, build_options):
        metal_storage = build_options['base_metal_storage']
        energy_storage = build_options['base_energy_storage']

        for ent in self.entities:
            metal_storage += ent.metal_storage
            energy_storage += ent.energy_storage
        
        