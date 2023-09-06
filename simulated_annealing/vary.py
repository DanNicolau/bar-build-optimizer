# the types of actions that can take place:


#   add action
# reclaim entity
# det com
# build entity

#   remove an action, but check legality first? maybe check legality after selection and make reselection if illegal
# remove a build legality issues:
#   removes the only builder of a type that was required to build something in the future
#   leaves a lone reclaim
#       
# 

# alternatively just check legality after and loop back to a different option

import random
from copy import copy
from dataclasses import dataclass
from simulated_annealing.utils import generate_current_entities, entity_counts, Action

# @dataclass()
# class Action:
#     type: str
#     entity: str


def possible_builds(current_entities, build_options):
    entity_str_set = set(current_entities)

    buildable = set()

    counts = entity_counts(current_entities)

    for current_ent_str in entity_str_set:
        ent = build_options['entity_library'][current_ent_str]
        for ent_str in ent.build_list:

            #ent_str is the ent we can build not accounting for counts rn
            if not ent_str in build_options['build_restrictions']:
                limit = 9001 if build_options['build_restrictions']['default_allow'] else 0
            else:
                limit = build_options['build_restrictions'][ent_str]

            current = counts[ent_str] if ent_str in counts else 0

            if limit - current > 0:
                buildable.add(Action('build', ent_str))

    return buildable

def possible_det_com(current_entities, build_options):
    if 'commander' in current_entities and not is_final_constructor(current_entities, build_options['entity_library'], 'commander'):
        return {Action('selfd','commander')}
    else:
        return {}
    
def is_final_constructor(current_entities, lib, ent_to_check):
    if len(lib[ent_to_check].build_list) == 0: # not a con case
        return False
    
    con_count = 0
    for ent in current_entities:
        if len(lib[ent].build_list) > 0:
            con_count += 1
        if con_count >= 2:
            return False

    return True

def has_reclaimers(current_entities, lib):
    for ent in current_entities:
        if lib[ent].is_reclaimer:
            return True
    return False

def possible_reclaims(current_entities, build_options):
    lib = build_options['entity_library']
    reclaim_actions = set()

    if not has_reclaimers(current_entities, build_options['entity_library']):
        return reclaim_actions

    for current_ent_str in current_entities:
        if is_final_constructor(current_entities, lib, current_ent_str):
            continue
        if lib[current_ent_str].is_reclaimable:
            reclaim_actions.add(Action('reclaim',current_ent_str))
    return reclaim_actions

def vary(current_solution, starting_entities, build_options):
    #generate all the possible variations
    possible_variations = set()
    current_entities = generate_current_entities(current_solution, starting_entities, build_options)

    build_actions = possible_builds(current_entities, build_options)
    possible_variations.update(build_actions) 

    det_com_actions = possible_det_com(current_entities, build_options)
    possible_variations.update(det_com_actions)

    reclaim_actions = possible_reclaims(current_entities, build_options)
    possible_variations.update(reclaim_actions)

    #randomly choose to add or remove a variation
    current_len = len(current_solution)

    choice = random.choice(tuple(possible_variations))

    new_sol = copy(current_solution)
    new_sol.append(choice)

    return new_sol