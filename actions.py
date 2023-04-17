import dataclasses
import setup_utils

def generate_available_actions(state):

    for entity in state.entities:

        if entity.is_builder:
            print(f'builders: {entity}')

    
def update_resources(state):

    updated_state = dataclasses.replace(state)

    total_metal_storage = state.base_metal_storage
    total_energy_storage = state.base_energy_storage
    metal_production = 0.0
    energy_production = 0.0

    for entity in state.entities:
        if entity.is_complete:
            total_metal_storage += entity.metal_storage
            total_energy_storage += entity.energy_storage
            metal_production += entity.metal_production
            energy_production += entity.energy_production

    #TODO update incomplete buildings constructions

    return updated_state

def generate_states(state, timestep=1.0):
    new_state = dataclasses.replace(state)
    
    #apply resource change by timestep
    update_resources(new_state)

    #todo verify above  works, does this need a deep copy? 

    actions = generate_available_actions(state) # each builder can start_build and help_build

    print(actions)

    new_states = []

    return new_states