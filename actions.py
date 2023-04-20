import dataclasses
import setup_utils

entity_library = setup_utils.load_entities()

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
            actions.append((entity.id, 'blow_com')) # will we ever have no builders? may need global idle with no builders

        if entity.is_builder:
            print(f'builders: {entity}')

            # all builders can idle
            actions.append( (entity.id, 'idle') )

            # all builders can start a build
            for build_option in entity.build_list:

                #get mex count and make sure we aren't fulfilled already
                if (build_option == 'mex'):
                    mex_count = 0
                    for ent in state.entities:
                        if (ent.id_string == 'mex'):
                            mex_count += 1
                    if mex_count >= state.available_mex:
                        continue

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

    print('ACTIONS')
    print(actions)

    for action in actions:
        new_state = simulate_action(state, action, timestep) # copy state inside
        new_states.append(new_state)

    return new_states

def simulate_start_build(action, state, timestep, tolerance=0.01):

    print(action)

    new_ent = dataclasses.replace(entity_library[action[2]])
    state.entities.append(new_ent)

    #need to subtract proportionate amount of resources
    builder = None
    for ent in state.entities:
        if (action[0] == ent.id):
            builder = ent
    buildpower = builder.build_power

    #gotta do some ratio math here to figure out how much to build the thing
    ratio = buildpower * timestep / new_ent.work_required
    metal_request_timestep = ratio * new_ent.cost_metal
    energy_request_timestep = ratio * new_ent.cost_energy

    if (metal_request_timestep <= state.metal and energy_request_timestep <= state.energy):
        #life is good spend the money and move on
        state.metal -= metal_request_timestep
        state.energy -= energy_request_timestep
        new_ent.work_completed += ratio

    elif (metal_request_timestep > state.metal and energy_request_timestep <= state.energy):
        #metal limited
        new_ratio = state.metal / new_ent.cost_metal
        state.metal = 0
        state.energy -= new_ratio * new_ent.cost_energy
        if (new_ratio > ratio):
            raise Exception("we misunderstood the metal math")

        new_ent.work_completed += new_ratio
        
    elif (energy_request_timestep > state.energy and metal_request_timestep <= state.metal):
        #energy limited
        new_ratio = state.energy / new_ent.cost_energy
        state.energy = 0
        state.metal -= new_ratio * new_ent.cost_metal
        if (new_ratio > ratio):
            raise Exception("we misunderstood the energy math")

    else:
        # both limited, find the most limiting and reduce accordingly (might replace above 2 cases)
        new_energy_ratio = state.energy / new_ent.cost_energy
        new_metal_ratio = state.metal / new_ent.cost_metal

        if (new_energy_ratio > ratio or new_metal_ratio > ratio):
            raise Exception("we really misunderstood the math")
        min_ratio = min([new_energy_ratio, new_metal_ratio])

        state.energy -= min_ratio * new_ent.cost_energy
        state.metal -= min_ratio * new_ent.cost_metal
        new_ent.work_completed += min_ratio

    if (new_ent.work_completed >= new_ent.work_required):
        new_ent.is_complete = True

#idle, blow_com, start_build, build_contribute, reclaim
# this must generate a new state, not point to the same state object
def simulate_action(state, action, timestep):

    new_state = dataclasses.replace(state)
    new_state.time_elapsed += timestep
    update_resources(new_state)

    if (action[1] == 'blow_com'):
        updated_entities = []
        for ent in new_state.entities:
            if ent.id != action[0]:
                updated_entities.append(ent)
        updated_entities.append(entity_library['commander_wreck'])
        new_state.entities = updated_entities
    elif (action[1] == 'idle'):
        pass
    elif (action[1] == 'start_build'):
        simulate_start_build(action, state, timestep)

    return new_state