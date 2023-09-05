import copy

from collections import namedtuple

Action = namedtuple('Action', ['type', 'entity'])

def generate_current_entities(current_solution, starting_entities, build_options):    
    current_entities = copy.copy(starting_entities)
    for action in current_solution:
        if (action.type == 'build'):
            current_entities.append(action.entity)
    return current_entities

def entity_counts(entities):
    counts = {}
    for e in entities:
        if not e in counts:
            counts[e] = 1
        else:
            counts[e] += 1
    return counts