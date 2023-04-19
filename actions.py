import dataclasses
import setup_utils


def get_incomplete_entities(state):
    incompletes = []
    for ent in state.entities:
        if (ent.is_complete == False):
            incompletes.append(ent)

    return incompletes


#idle, blow_com, start_build, build_contribute, reclaim

def generate_available_actions(state):

    actions = []

    # get incomplete things
    incomplete_entities = get_incomplete_entities(state)

    for entity in state.entities:

        if entity.id_string == 'commander':
            actions.append((entity.id, 'blow_com'))

        if entity.is_builder:
            print(f'builders: {entity}')

            # all builders can idle
            actions.append( (entity.id, 'idle') )

            # all builders can start a build
            for build_option in entity.build_list:
                actions.append( (entity.id, 'start_build', build_option) )

            # all builders can build_contribute
            for inc_ent in incomplete_entities:
                actions.append( (entity.id, 'build_contribute', inc_ent.id) )

            # all builders can reclaim other things
            for rec_ent in state.entities:
                if (rec_ent.is_reclaimable and rec_ent.id != entity.id):
                    actions.append( (entity.id, 'reclaim', rec_ent.id) )

    return actions

    
def update_resources(state):

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

    state.metal += metal_production
    if (state.metal > total_metal_storage):
        state.metal = total_metal_storage
    state.energy += energy_production
    if (state.energy > total_energy_storage):
        state.energy = total_energy_storage

def generate_states(state, timestep=1.0):
    new_states = []
    actions = generate_available_actions(state) # each builder can start_build and help_build

    for action in actions:
        new_state = simulate_action(state, action, timestep) # copy state inside
        new_states.append(new_state)


    #remove states after time 3
    filtered_states = []
    for new_state in new_states:
        if (new_state.time_elapsed < 3):
            filtered_states.append(new_state)

    print(filtered_states)

    return filtered_states

#idle, blow_com, start_build, build_contribute, reclaim
def simulate_action(state, action, timestep):

    new_state = dataclasses.replace(state)
    new_state.time_elapsed += timestep
    update_resources(new_state)

    print(action)

    if (action[1] == 'blow_com'):
        updated_entities = []
        for ent in new_state.entities:
            if ent.id != action[0]:
                updated_entities.append(ent)
        updated_entities.append(setup_utils.load_entities()['commander_wreck'])
        new_state.entities = updated_entities
    elif (action[1] == 'idle'):
        pass

    return new_state