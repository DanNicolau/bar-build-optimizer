import copy

from collections import namedtuple
from dataclasses import dataclass

Action = namedtuple('Action', ['type', 'entity'])

@dataclass
class Variation:
    action: Action # None for removal
    idx: int # -1 for append?
    type: str # add, removal

def entity_counts(entities):
    counts = {}
    for e in entities:
        counts[e] = 1 if not e in counts else counts[e] + 1
    return counts

def print_actions(actions: list):
    for i, a in enumerate(actions):
        print(f'{i+1}: {a.type} {a.entity}')

def update_counts(counts, action):
    if action.type == 'build':
        counts[action.entity] = 1 if not action.entity in counts else counts[action.entity] + 1
    elif action.type == 'reclaim' or (action.type == 'selfd' and action.entity != 'commander'):
        if (not action.entity in counts) or counts[action.entity] < 0:
            print(counts)
            raise ValueError("cannot have negative or reclaim nonexistent entity")
        else:
            counts[action.entity] -= 1
    elif action.type == 'selfd' and action.entity == 'commander':
        if not 'commander_wreck' in counts:
            counts['commander'] -= 1
            counts['commander_wreck'] = 1
        else:
            counts['commander'] -= 1
            counts['commander_wreck'] += 1

def count_sum(counts):
    sum = 0
    for ent in counts:
        sum += counts[ent]
    return sum