from dataclasses import dataclass, field, replace
from itertools import count
from Entity import *

@dataclass
class TeamState:
    entities: Dict[int, Entity]
    id: int = field(default_factory=count().__next__, init=False)
    # available_mex: int = field(default = 3) # check mex doesn't exceed this
    metal: float = field(default = 0)
    energy: float = field(default = 0)
    time_elapsed: float = field(default = 0)

    def __repr__(self):
        return f'STATE {self.id} | time: {self.time_elapsed} | {self.metal}m {self.energy}e | {self.hash()}\n'
    
    def new_state(self, new_id=True):
        new_state = replace(self)
        new_state.entities = {}
        for ent_id, ent in self.entities.items():
            new_ent = replace(ent)
            new_ent.id = ent_id
            new_state.entities[ent_id] = new_ent
        return new_state
    
    def hash(self):
        entity_strings = []
        for ent_id, ent in self.entities.items():
            entity_strings.append(ent.id_string)
        entity_strings.sort()
        h = ','.join(entity_strings)
        return h
    
    def get_builders(self):
        builders = []
        for ent_id, ent in self.entities.items():
            if (ent.is_builder):
                builders.append(ent)
        return builders
    
    def get_total_buildpower(self):
        build_power = 0
        for ent_id, ent in self.entities.items():
            if (ent.is_builder):
                build_power += ent.build_power
        return build_power
    
    def get_build_options(self):
        build_options = {}
        for builder in self.get_builders():
            for build_option in builder.build_list:
                if not build_option in build_options:
                    build_options[build_option] = builder.build_list[build_option]
        return build_options

    def get_metal_production(self):
        m_prod = 0
        for ent_id, ent in self.entities.items():
            m_prod += ent.metal_production
        return m_prod
    

    def time_to_generate_metal(self, cost_metal):
        if (self.metal >= cost_metal):
            return 0
        
        m_prod = self.get_metal_production()

        if(m_prod <= 0):
            raise ValueError("metal prod is negative or 0, goal will never be reached")
        else:
            ttm = (cost_metal - self.metal) / m_prod
            return ttm
        
    def get_energy_production(self):
        e_prod = 0
        for ent_id, ent in self.entities.items():
            e_prod += ent.energy_production
        return e_prod
    
    def time_to_generate_energy(self, cost_energy):
        if (self.energy >= cost_energy):
            return 0
        
        e_prod = self.get_energy_production()

        if (e_prod <= 0):
            raise ValueError("energy prod is negative or 0, goal will never be reached")
        else:
            tte = (cost_energy - self.energy) / e_prod
            return tte
            
    def elapse_time(self, time):
        self.metal += self.get_metal_production() * time
        self.energy += self.get_energy_production() * time
        self.time_elapsed += time

    def construct_building(self, building):
        new_building = replace(building)
        self.entities[new_building.id] = new_building
        self.metal -= new_building.cost_metal
        self.energy -= new_building.cost_energy

    #return True if we are build restricted
    def check_build_restricted(self, build_str, options):
        restrictions = options['build_restrictions']

        for ent_id, ent in self.entities.items():
            if (ent.id_string in restrictions):
                restrictions[ent.id_string] -= 1
        if (build_str in restrictions):
            restrictions[build_str] -= 1
            if (restrictions[build_str] == 0):
                return True
        return False


    def get_com(self):
        for ent_id, ent in self.entities.items():
            if (ent.id_string == 'commander'):
                return ent
        return None

    def blow_com(self, wreck):

        com = self.get_com()
        self.entities.pop(com.id)
        new_wreck = replace(wreck)
        self.entities[new_wreck.id] = new_wreck

    def sim_build(self, ent_to_build, options):
        
        if (ent_to_build.id_string == 'commander_wreck'):
            print(ent_to_build)
            self.blow_com(ent_to_build)
            self.elapse_time(options['time_to_blow_com'])
        else:
            ttw = ent_to_build.work_required / self.get_total_buildpower()

            try:
                ttm = self.time_to_generate_metal(ent_to_build.cost_metal)
                tte = self.time_to_generate_energy(ent_to_build.cost_energy)
            except ValueError as ve:
                return False

            # print(f'times: {ttw}, {ttm}, {tte}')
            time_to_build = max(ttm, tte, ttw)

            self.elapse_time(time_to_build)
            self.construct_building(ent_to_build)
        return True

    def generate_neighbours(self, options):
        neighbours = []
        #for each thing we can build, that is a neighbour state, can figure out time and resource cost later
        build_options = self.get_build_options()
        for build_str, build_option in build_options.items():

            # TODO metal and geo limits should go here
            # if (build_str == 'mex' and not self.can_build_mex(options)):
            #     continue

            if (self.check_build_restricted(build_str, options)):
                continue

            neighbour = self.new_state()
            success = neighbour.sim_build(build_option, options)
            if (success):
                neighbours.append(neighbour)

        return neighbours
    
    def is_goal(self, desired_entities):
        desired_counts = {}
        found_counts = {}
        for d_ent in desired_entities:
            if not d_ent in desired_counts:
                desired_counts[d_ent] = 1
                found_counts[d_ent] = 0
            else:
                desired_counts[d_ent] += 1
        
        for ent_id, ent in self.entities.items():
            if ent.id_string in found_counts:
                found_counts[ent.id_string] += 1

        for idx, count in found_counts.items():
            if count < desired_counts[idx]:
                return False
        
        return True