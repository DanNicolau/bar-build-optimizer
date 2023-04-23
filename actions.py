import dataclasses
import setup_utils


# def increment_resources(state, options):
#     total_metal_production = 0
#     total_energy_production = 0
#     total_energy_storage = options['base_energy_storage']
#     total_metal_storage = options['base_metal_storage']

#     for id, ent in state.entities.items():
#         total_metal_production += ent.metal_production
#         total_energy_production += ent.energy_production
#         total_energy_storage += ent.energy_storage
#         total_metal_storage += ent.metal_storage

#     state.metal += total_metal_production * options['timestep']
#     state.energy += total_energy_production * options['timestep']

#     state.metal if state.metal <= total_metal_storage else total_metal_storage
#     state.energy if state.energy <= total_energy_storage else total_energy_storage

# def increment_build_progress(state, options):
    
#     build_pairs = []

#     for id, ent in state.entities.items():
#         if ent.is_builder and ent.build_target > 0:
#             build_pairs.append((ent, state.entities[ent.build_target]))

# def increment_state(state, options):
#     # keep building anything we are building
#     new_state = dataclasses.replace(state)
#     new_state.time_elapsed += options['timestep']

#     increment_resources(new_state, options)
#     increment_build_progress(new_state, options)

#     return new_state

def generate_states(state, options):
    #get total build list
    #build something if we have an incomplete building available
    builders = []
    incomplete_entities = []
    new_states = [state.new_state()]
    for ent_id, ent in state.entities.items():
        if (ent.is_builder and ent.is_complete and ent.build_target == -1): # TODO build target condition may need to be updated
            builders.append(ent)
        if (not ent.is_complete):
            incomplete_entities.append(ent)
   
    #we can add a state for every possible build option
    build_options = {}
    for builder in builders:
        for str_id, build_option in builder.build_list.items():
            if (not (build_option.id_string in build_options)):
                build_options[build_option.id_string] = build_option

    new_building_srcs = []

    for id_str, build_option in build_options.items():
        new_building_srcs.append(build_option)

    # get available builders
    available_builder_ids = []
    for builder in builders:
        if (builder.build_target == -1):
            available_builder_ids.append(builder.id)

    # print(f'available_builders: {available_builder_ids}')

    # every available builder and build item combo is a new state
    # need to make sure that we clone builder so we are not just modifying the same reference to a builder on every iter
    for available_builder_id in available_builder_ids:
        for new_building_src in new_building_srcs:

            new_state = state.new_state()
            new_building = new_building_src.new_building(new_id=True)
            new_state.entities[new_building.id] = new_building
            new_state.entities[available_builder_id].build_target = new_building.id
            new_states.append(new_state)
            
    #increment time, resources, and build on new states
    for ns in new_states:
        ns.advance(options)

    print('NEW STATES')
    print(new_states)



    return new_states

    
