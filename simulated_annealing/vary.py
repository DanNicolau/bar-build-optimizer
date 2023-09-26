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
from copy import copy, deepcopy
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
    
def check_only_positive_ent_counts_after_update(test_counts):
    for ent in test_counts:
        if test_counts[ent] < 0:
            return False

def is_legal_reclaim_at_idx(solution, variation, initial_counts):
    test_solution = copy(solution)
    test_solution.insert(variation.idx, variation.action)

    test_counts = copy(initial_counts)

    for action in test_solution:
        update_counts(test_counts, action)
        if not check_only_positive_ent_counts_after_update(test_counts):
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
        if len(reclaimers) == 1 and lib[reclaimable].is_reclaimer: # is this even correct?... yes it is read it carefully
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

def check_legal_selfd_at_action_before_count_update(action, test_counts):
    if action.type == 'selfd' and action.entity == 'commander':
        if test_counts['commander'] == 0:
            return False # TODO this changes if rez can occur
        
def check_legal_selfd_at_action_after_count_update(test_counts, lib):
    final_con_count = 0
    for ent in test_counts:
        if lib[ent].is_possible_final_constructor:
            final_con_count += test_counts[ent]

    if final_con_count < 1:
        return False

# only illegal if there is no commander to blow up or if it is the final con
def is_legal_selfd(solution, starting_counts, variation, lib):
    test_solution = copy(solution)
    test_counts = copy(starting_counts)

    #must have the commander and also must not create a negative count in the future for any final cons
    test_solution.insert(variation.idx, variation.action)

    for action in test_solution:
        if not check_legal_selfd_at_action_before_count_update(action, test_counts):
            return False
        update_counts(test_counts, action)
        if not check_legal_selfd_at_action_after_count_update(test_counts, lib):
            return False

    return True


#basically if the com is not the last constructor, consider det the com
def selfd_com_additions(current_solution, starting_entities, build_options):
    variations = []
    lib = build_options['entity_library']
    counts = entity_counts(starting_entities)

    # print(current_solution)

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

    # print('selfd variations')
    
    # print(variations)

    return variations



def add_step_to_build_order_possibilities(current_solution, starting_entities, build_options):
    variations = []
    variations += build_step_additions(current_solution, starting_entities, build_options)
    variations += reclaim_step_additions(current_solution, starting_entities, build_options)
    variations += selfd_com_additions(current_solution, starting_entities, build_options)
    
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

    elif variation.type == 'remove':
        # print(f'pre del: ({len(new_solution)}) {new_solution}')
        del new_solution[variation.idx]
        # print(f'\tREMOVED w {variation}')
        # print(f'after del ({len(new_solution)}): {new_solution}')
        return new_solution
    else:
        raise ValueError('Unknown variation type')

# need to check legal reclaim
# need to check legal selfd
# need to check is under ent max
# need to check if is buildable 
# at every index
def is_legal_remove(current_solution, starting_entities, new_variation, build_options):
    test_counts = entity_counts(starting_entities)
    test_solution = copy(current_solution)
    lib = build_options['entity_library']

    # print('old test sol')
    # print(test_solution)

    del test_solution[new_variation.idx]

    # print('new test sol: ')
    # print(test_solution)

    # we don't need to check idx 0, can assume we start with a legal state

    # check every action after
    for action in test_solution:
        #                                   need to check legal selfds
        if action.type == 'selfd':
            if not check_legal_selfd_at_action_before_count_update():
                return False
        update_counts(test_counts, action)
        if action.type == 'selfd':
            # this rule should hold after any action anyway
            if not check_legal_selfd_at_action_after_count_update(test_counts, lib):
                return False

        

        #                                   reclaims:


        # #   ensure a reclaimer is available and is not reclaiming itself

        if action.type == 'reclaim':
            reclaimers = filter_reclaimers(test_counts, lib)
            if len(reclaimers) < 1:
                return False
            # make sure last reclaimer not reclaiming itself
            elif len(reclaimers) == 1:
                reclaimables = generate_reclaimables(test_counts, lib)
                for reclaimer in reclaimers:
                    if len(reclaimables) == 1 and reclaimer in reclaimables:
                        return False
        # #   counts don't go under 0
        for ent in test_counts:
            if test_counts[ent] < 0:
                return False

        # need to check is under ent maxs
        maxes = build_options['build_restrictions']
        for ent in test_counts:
            if ent in maxes and test_counts[ent] > maxes[ent]:
                return False
            elif (not ent in maxes) and (not maxes['default_allow']):
                return False

        # need to check if buildable rules have been followed
        if action.type == 'build':
            build_list = set()
            for ent in test_counts:
                for buildable in lib[ent].build_list:
                    build_list.add(buildable)

            build_list = list(build_list)
            if not action.entity in build_list:
                return False

    return True


# basically: try to remove a variation - check the ent count rule, the builder rule, the build list rules
def remove_step_from_build_order_possibilities(current_solution, starting_entities, build_options):
    variations = []

    for i, action in enumerate(current_solution):
        # print(action)
        new_variation = Variation(None, i, 'remove')
        if is_legal_remove(current_solution, starting_entities, new_variation, build_options):
            variations.append(new_variation)

    return variations

def vary(current_solution, starting_entities, build_options):
    
    variations = []
    variations += add_step_to_build_order_possibilities(current_solution, starting_entities, build_options)
    variations += remove_step_from_build_order_possibilities(current_solution, starting_entities, build_options)

    # print(variations)

    #choose a variation
    if len(variations) == 0:
        #this should not occur, we must be able to backtrack a build with a remove or a remove with a build
        raise ValueError('No variations...')

    chosen_variation = random.choice(variations)

    # print(f'chosen_variation: {chosen_variation}')


    #apply the variation
    # print(f'\nold sol ({len(current_solution)}): {current_solution}')
    new_solution = apply_variation(current_solution, chosen_variation)
    # print(f'new sol ({len(new_solution)}): {new_solution}')
    # print(f'new sol:')
    # for i, action in enumerate(new_solution):
        # print(i, action.type, action.entity, sep='\t')

    return new_solution