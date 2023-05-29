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