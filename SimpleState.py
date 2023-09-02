from dataclasses import dataclass
from Entity import Entity
from typing import List, Dict

@dataclass
class SimpleState:
    entities: List[str]
    metal: float
    energy: float

    def get_production(self, build_options):
        metal_prod = 0.0
        energy_prod = 0.0
        lib = build_options['entity_library']
        for ent in self.entities:
            e = lib[ent]
            metal_prod += e.metal_production
            energy_prod += e.energy_production
        return metal_prod, energy_prod

    def get_buildpower(self, ent_to_build: Entity, build_options: Dict):
        
        #get best factory builder that exists in ents that builds the ent_to_build
        ent_str = ent_to_build.id_string
        built_by = build_options['built_by']
        lib = build_options['entity_library']

        best_factory_bp = 0
        for built_from in built_by[ent_str]:
            if not lib[built_from].is_factory:
                continue
            if not built_from in self.entities:
                continue
            new_factory_bp = lib[built_from].build_power
            best_factory_bp = best_factory_bp if best_factory_bp > factory_bp else new_factory_bp

        total_bp = best_factory_bp            

        for ent_str in self.entities:
            e = lib[ent_str]
            if e.is_builder and not e.is_factory:
                total_bp += e.build_power 

        return total_bp

    def get_storage(self, build_options):
        metal_storage = build_options['base_metal_storage']
        energy_storage = build_options['base_energy_storage']

        for ent in self.entities:
            metal_storage += ent.metal_storage
            energy_storage += ent.energy_storage
        
    def time_to_work(self, ent_to_build: Entity, build_power: float):
        return ent_to_build.work_required / build_power
    
    def time_to_metal(self, ent_to_build: Entity):
        exit(-1)

    #returns triplet of resources that need to be generated 
    def time_to_generate_resources(self, ent_to_build, build_options):
        #time to generate metal

        build_power = self.get_buildpower(ent_to_build, build_options)
        prod = self.get_production(build_options)

        ttw = self.time_to_work(ent_to_build, build_power)
        ttm = self.time_to_metal(ent_to_build, prod[0])
        tte = self.time_to_energy(ent_to_build, prod[1])


        raise NotImplementedError()