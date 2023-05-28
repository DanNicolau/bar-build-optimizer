from BuildOrder import BuildOrder
from dataclasses import dataclass

@dataclass
class Solution:
    build_order: BuildOrder
    score: float