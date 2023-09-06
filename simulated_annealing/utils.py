import copy

from collections import namedtuple

Action = namedtuple('Action', ['type', 'entity'])

def generate_current_entities(current_solution, starting_entities, build_options):    
    current_entities = copy.copy(starting_entities)
    for action in current_solution:
        if (action.type == 'build'):
            current_entities.append(action.entity)
        elif (action.type == 'reclaim' or action.type == 'selfd'):
            #remove an entity of the correct type, otherwise throw an error
            for i in range(len(current_entities)):
                print(action.entity)
                print(current_entities)
                print('\n')
                current_entities.remove(action.entity)
                break

    return current_entities

def entity_counts(entities):
    counts = {}
    for e in entities:
        if not e in counts:
            counts[e] = 1
        else:
            counts[e] += 1
    return counts