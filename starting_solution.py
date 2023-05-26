from BuildOrder import BuildOrder
from Entity import Entity
from typing import Dict, List

def include_in_build(current_ents, desired_ent, built_by):

    print('here')
    print(desired_ent)

    built_by_ents =  built_by[desired_ent]
    for (built_by_ent in current_ents)
    if built_by_ent in current_ents:
        current_ents.append(desired_ent)
    else:
        for built_by_ent in built_by_ents:
            include_in_build(current_ents, built_by_ent, built_by)

    print(current_ents)
    exit()

def generate_starting_solution(starting_entities: List[Entity], desired_entities: List, build_options: Dict):
    
    # build_order = BuildOrder(
    #     starting_entities=starting_entities,
    #     action_list=[]
    # )

    built_by = build_options['built_by']
    current_entities = starting_entities.copy()

    for desired_ent in desired_entities:
        include_in_build(current_entities, desired_ent, built_by)

    print(current_entities)

    exit(0)
    #table of what is built by what is in the build options

    return []