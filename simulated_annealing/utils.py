import copy

def generate_current_entities(current_solution, starting_entities, build_options):    
    current_entities = copy.copy(starting_entities)
    for action in current_solution:
        if (action.type == 'build'):
            current_entities.append(action.entity)
    return current_entities