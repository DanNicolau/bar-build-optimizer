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
    if 'commander' in current_entities:
        return {Action('selfd','commander')}
    else:
        return {}
    
def possible_reclaims(current_entities, build_options):
    lib = build_options['entity_library']
    reclaim_actions = set()
    for current_ent_str in current_entities:
        if lib[current_ent_str].is_reclaimable:
            reclaim_actions.add(Action('reclaim',current_ent_str))

    print(reclaim_actions)
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

    #

    print('what')
    print(possible_variations)

    exit()