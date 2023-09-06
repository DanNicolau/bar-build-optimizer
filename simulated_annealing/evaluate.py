from simulated_annealing.utils import entity_counts

def is_valid_solution(solution, desired_entities):

    desired_entities_counts = entity_counts(desired_entities)

    running_ent_count = {}

    for action in solution:
        if action.entity in desired_entities:
            if not action.entity in running_ent_count:
                running_ent_count[action.entity] = 1
                if action.type != 'build':
                    raise ValueError()
            else:
                running_ent_count[action.entity] += 1 if action.type == 'build' else -1

    print(f'sol: {solution}')
    for d in desired_entities_counts:
        print(f'd: {d}')
        if not d in running_ent_count:
            print('no ent found in count')
            return False
        if running_ent_count[d] < desired_entities_counts[d]:
            print('too few found')
            return False
    return True

# lower is better
def evaluate(solution, desired_entities):

    if not is_valid_solution(solution, desired_entities):
        return 4294967295.0 # arbitrarily large numb

    return len(solution)

    time_to_build = 0
    # for action in solution:
    #     time_to_build += time_to_complete_action(action)


    return time_to_build

# greedy for now
# theres room to further optimize by caching the score of the previous best solution
def accept(current_solution_score, proposed_solution, desired_entities, build_options):

    proposed_solution_score = evaluate(proposed_solution, desired_entities)

    if proposed_solution_score <= current_solution_score:
        return True, proposed_solution_score
    else:
        return False, proposed_solution_score