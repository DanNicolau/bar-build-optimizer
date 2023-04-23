from dataclasses import dataclass, field, replace
from typing import List, Dict
from itertools import count

def advance_entity_build_progress(state, builder, ent, options):
    if (ent.is_complete):
        print(f'state: {state}, builder: {builder}, ent: {ent}')
        raise ValueError("this should not be a build target if it is complete!")
    
    print('ADVANCE BUILD')
    print(state)
    print(builder)
    print(ent)

    build_timestep = builder.build_power * options['timestep']

    ratio = build_timestep / ent.work_required
    ratio = min(1, ratio)

    m_required = ratio * ent.cost_metal
    e_required = ratio * ent.cost_energy
    if (m_required > state.metal or e_required > state.energy):
        return

    ent.work_completed += build_timestep
    # to be fair this can be handled earlier...
    if (ent.work_completed >= ent.work_required): # build done case
        ent.is_complete = True
        builder.build_target = -1
        ratio = ratio - (ent.work_completed - ent.work_required)/ent.work_required # sub extra work from ratio
        if (ratio < 0):
            print(f'builder: {builder}, ent: {ent}, ratio: {ratio}')
            raise ValueError("should not be adding resources after a build step")

    state.metal -= ratio * ent.cost_metal
    state.energy -= ratio * ent.cost_energy

@dataclass
class Entity:
    id_string: str
    is_building: bool
    id: int = field(default_factory=count().__next__, init=False)
    is_builder: bool = field(default = False)
    build_list: Dict = field(default_factory = lambda: {})
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
    is_reclaimable: bool = field(default = True)
    build_target: int = field(default = -1)

    def __repr__(self):
        return f'ent{self.id}-{self.id_string}-{min(100, self.work_completed/self.work_required*100)}%-b:{self.build_target} '
    
    def new_building(self, new_id=True):
        old_id = self.id
        new_building = replace(self)
        new_building.is_complete = False
        new_building.work_completed = 0.0

        if not new_id:
            new_building.id = old_id

        return new_building

@dataclass
class TeamState:
    entities: Dict[int, Entity]
    parent: int
    id: int = field(default_factory=count().__next__, init=False)
    # available_mex: int = field(default = 3) # check mex doesn't exceed this
    metal: float = field(default = 0)
    energy: float = field(default = 0)
    time_elapsed: float = field(default = 0)

    def __repr__(self):
        return f'STATE {self.id} | time: {self.time_elapsed} | {self.metal}m {self.energy}e | {self.entities} | p:{self.parent}\n'
    
    def new_state(self, new_id=True):
        new_state = replace(self)
        new_state.parent = self.id
        new_state.entities = {}
        for ent_id, ent in self.entities.items():
            new_ent = replace(ent)
            new_ent.id = ent_id
            new_state.entities[ent_id] = new_ent
        return new_state
    
    def increment_resources(self, options):
        total_metal_production = 0
        total_energy_production = 0
        total_energy_storage = options['base_energy_storage']
        total_metal_storage = options['base_metal_storage']

        for id, ent in self.entities.items():
            if not ent.is_complete:
                continue
            total_metal_production += ent.metal_production
            total_energy_production += ent.energy_production
            total_energy_storage += ent.energy_storage
            total_metal_storage += ent.metal_storage

        self.metal += total_metal_production * options['timestep']
        self.energy += total_energy_production * options['timestep']

        self.metal = min(self.metal, total_metal_storage)
        self.energy = min(self.energy, total_energy_storage)
    
    def increment_builds(self, options):
        builders = []
        for ent_id, ent in self.entities.items():
            if (ent.is_builder and ent.is_complete):
                builders.append(ent)

        for builder in builders:
            if builder.build_target == -1:
                continue
            ent = self.entities[builder.build_target]
            advance_entity_build_progress(self, builder, ent, options)

    def advance(self, options):
        self.time_elapsed += options['timestep']
        self.increment_resources(options)
        self.increment_builds(options)
        
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