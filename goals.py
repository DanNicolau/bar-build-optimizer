def goal_criteria_met(desired_entities, state):
    
    criteria_counts = {}

    for ent in desired_entities:
        if (ent in criteria_counts):
            criteria_counts[ent] += 1
        else:
            criteria_counts[ent] = 1

    found_counts = {}

    for ent in criteria_counts:
        found_counts[ent] = 0

    for ent in state.entities:
        if (ent.id_string in found_counts and ent.is_complete):
            found_counts[ent.id_string] += 1

    print(criteria_counts)
    print(found_counts)

    for ent in criteria_counts:
        if (not (ent in found_counts)): # if we haven't found the criteria one then just ret false
            return False
        if (found_counts[ent] < criteria_counts[ent]):
            return False
    return True