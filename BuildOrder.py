from dataclasses import dataclass
from typing import List, Dict

@dataclass
class BuildOrder:

    starting_entities: List
    action_list: List # actions are build:x, reclaim":x, selfdcom

    

    def get_time_to_complete(self, build_options: Dict):
        raise NotImplementedError()
    
    def build(self, ent_str):
        self.action_list.append(f'build:{ent_str}')

    def reclaim(self, ent_str):
        self.action_list.append(f'reclaim:{ent_str}')

    def self_d(self, ent_str):
        self.action_list.append('selfdcom')