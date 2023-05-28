from BuildOrder import BuildOrder
from Entity import Entity
from typing import Dict, List

def include_in_build(current_ents, desired_ent, built_by):
    raise NotImplementedError()


def generate_starting_build(starting_entities: List[Entity], desired_entities: List, build_options: Dict):
    
    build_order = BuildOrder(
        starting_entities=starting_entities,
        action_list=[]
    )

    return build_order

    built_by = build_options['built_by']
    current_entities = starting_entities.copy()

    for desired_ent in desired_entities:
        include_in_build(current_entities, desired_ent, built_by)

    #hack for an initial solution: just add the t1 and t2 cons and labs


    print(current_entities)

    exit()
    #table of what is built by what is in the build options

    return []