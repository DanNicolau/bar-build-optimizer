from BuildOrder import BuildOrder
from dataclasses import dataclass

@dataclass
#why is this even a dataclass
#TODO remove this random layer
class Solution:
    build_order: BuildOrder
    score: float