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
from simulated_annealing.utils import entity_counts, update_counts, count_sum, Action, Variation

def generate_build_list(counts, lib):
    build_list = set()
    for ent in counts:
        for buildable in lib[ent].build_list:
            build_list.add(buildable)

    return list(build_list)

def is_under_ent_maxes(current_solution, initial_counts, variation, build_options):
    maxes = build_options['build_restrictions']
    counts = copy(initial_counts)
    test_solution = copy(current_solution)
    test_solution.insert(variation.idx, variation.action)

    default_allow = maxes['default_allow']
    # print(f'\t in iuem')
    # print(f'{counts}')
    # print(f'{maxes}')

    for action in test_solution:
        update_counts(counts, action)

        # print(f'checking_action: {action}')

        for ent in counts:
            # print(f'checking_ent: {ent}')
            if ent in maxes and counts[ent] > maxes[ent]:
                # print(f'too many {ent}')
                return False
            # TODO handle default allow
            if (not ent in maxes) and (not default_allow):
                return False

    return True

def build_step_additions(current_solution, starting_entities, build_options):

    variations = []
    lib = build_options['entity_library']
    counts = entity_counts(starting_entities)
    initial_counts = copy(counts)

    # generate variations at idx 0
    build_list = generate_build_list(counts, lib)
    for buildable in build_list:
        new_action = Action('build', buildable)
        new_variation = Variation(new_action, 0, 'add')
        if is_under_ent_maxes(current_solution, initial_counts, new_variation, build_options):
            variations.append(new_variation)

    # generate legal variations after every action is performed
    for i in range(len(current_solution)):
        action = current_solution[i]
        #update counts
        update_counts(counts, action)
        build_list = generate_build_list(counts, lib)
        for buildable in build_list:
            new_action = Action('build', buildable)
            new_variation = Variation(new_action, i+1, 'add')
            if is_under_ent_maxes(current_solution, initial_counts, new_variation, build_options):
                variations.append(new_variation)

    return variations

def filter_reclaimers(counts, lib):
    r = {}
    for ent in counts:
        if counts[ent] > 0 and lib[ent].is_reclaimer:
            r[ent] = counts[ent]
    return r

def generate_reclaimables(counts, lib):
    reclaimables = []
    
    for ent in counts:
        if lib[ent].is_reclaimable and counts[ent] > 0:
            reclaimables.append(ent)

    return reclaimables
    

def is_legal_reclaim_at_idx(solution, variation, initial_counts):
    test_solution = copy(solution)
    test_solution.insert(variation.idx, variation.action)

    test_counts = copy(initial_counts)

    for action in test_solution:
        update_counts(test_counts, action)
        for ent in test_counts:
            if test_counts[ent] < 0:
                return False

    return True

#THE ISSUE

# we create a legal reclaim at the current action we are iterating in the solution, HOWEVER as actions are completed, a further reclaim becomes illegal
# proposed solution:
# check to see if the count goes negative after a simulated reclaim, if it does, then do not propose that variation

def reclaim_step_additions(current_solution, starting_entities, build_options):
    variations = []
    lib = build_options['entity_library']
    counts = entity_counts(starting_entities)
    initial_counts = copy(counts)

    # generate reclaims at idx 0
    # check for a reclaimer
    # check to make sure the last reclaimer is not reclaiming itself? (or last builder?)
    reclaimers = filter_reclaimers(counts, lib)
    reclaimables = generate_reclaimables(counts, lib)
    for reclaimable in reclaimables:
        # so long as this is not the last reclaimer we are ok
        if len(reclaimers) == 1 and lib[reclaimable].is_reclaimer:
            continue
        
        new_action = Action('reclaim', reclaimable)
        new_variation = Variation(new_action, 0, 'add')

        if is_legal_reclaim_at_idx(current_solution, new_variation, initial_counts):
            variations.append(new_variation)


    # print(reclaimers)
    # print(reclaimables)

    # generate reclaims after every single action
    for i, action in enumerate(current_solution):
        #update counts
        update_counts(counts, action)
        reclaimers = filter_reclaimers(counts, lib)
        reclaimables = generate_reclaimables(counts, lib)

        for reclaimable in reclaimables:
            if len(reclaimers) == 1 and lib[reclaimable].is_reclaimer:
                continue

            new_action = Action('reclaim', reclaimable)
            new_variation = Variation(new_action, i+1, 'add')
            if is_legal_reclaim_at_idx(current_solution, new_variation, initial_counts):
                variations.append(new_variation)

            
    return variations

# only illegal if there is no commander to blow up or if it is the final con
def is_legal_selfd(solution, starting_counts, variation, lib):
    print('\t\t in ilsd')
    test_solution = copy(solution)
    test_counts = copy(starting_counts)

    #must have the commander and also must not create a negative count in the future for any final cons
    test_solution.insert(variation.idx, variation.action)

    for action in test_solution:
        if action.type == 'selfd' and action.entity == 'commander':
            print('REACHED')
            print(test_counts['commander'])
            if test_counts['commander'] == 0:
                print('no commander to blow up')
                return False # TODO this changes if rez can occur
        
        update_counts(test_counts, action)

        final_con_count = 0
        for ent in test_counts:
            if lib[ent].is_possible_final_constructor:
                final_con_count += test_counts[ent]

        if final_con_count < 1:
            return False
    
    print('\t\t\t\t NOTHING WRONG')

    return True


#basically if the com is not the last constructor, consider det the com
def selfd_com_additions(current_solution, starting_entities, build_options):
    variations = []
    lib = build_options['entity_library']
    counts = entity_counts(starting_entities)

    print(current_solution)

    # idx 0
    new_action = Action('selfd','commander')
    new_variation = Variation(new_action, 0, 'add')
    if is_legal_selfd(current_solution, counts, new_variation, lib):
        variations.append(new_variation)


    # after every action
    for i, action in enumerate(current_solution):
        new_variation = Variation(new_action, i+1, 'add')
        if is_legal_selfd(current_solution, counts, new_variation, lib):
            variations.append(new_variation)

    print('selfd variations')
    
    print(variations)

    return variations



def add_step_to_build_order_possibilities(current_solution, starting_entities, build_options):
    variations = []
    variations += build_step_additions(current_solution, starting_entities, build_options)
    variations += reclaim_step_additions(current_solution, starting_entities, build_options)
    variations += selfd_com_additions(current_solution, starting_entities, build_options)
    
    return variations

def remove_step_from_build_order_possibilities():
    variations = []
    return variations

def apply_variation(current_solution, variation):
    new_solution = copy(current_solution)
    if len(current_solution) < variation.idx:
        raise ValueError("can't inject variation at nonexistent index")
    if variation.type == 'add':
        if variation.action == 'selfd':
            raise NotImplementedError()
        new_solution.insert(variation.idx, variation.action)
        return new_solution

    else:
        raise NotImplementedError()

def vary(current_solution, starting_entities, build_options):
    
    variations = []
    variations += add_step_to_build_order_possibilities(current_solution, starting_entities, build_options)
    variations += remove_step_from_build_order_possibilities()

    #choose a variation
    if len(variations) == 0:
        raise ValueError('No variations...')

    chosen_variation = random.choice(variations)
    print(f'chosen_variation: {chosen_variation}')


    #apply the variation
    new_solution = apply_variation(current_solution, chosen_variation)
    print(f'new sol:')
    for i, action in enumerate(new_solution):
        print(i, action.type, action.entity, sep='\t')

    return new_solution