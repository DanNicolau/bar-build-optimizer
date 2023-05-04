from dataclasses import dataclass, field
from TeamState import *

@dataclass
class Cost:
    state_id: int # -1 is not from a parent, starting cost or cost limit or something
    time_elapsed: float
    metal: float
    energy: float

    def is_dominated_by(self, other_cost):
        return other_cost.time_elapsed < self.time_elapsed #todo
    
    def __init__(self, state_id, time_elapsed: float, metal: float = 0, energy: float = 0):
        self.state_id = state_id
        self.time_elapsed = time_elapsed
        self.metal = metal
        self.energy = energy

    def from_state(state: TeamState):
        return Cost(state_id=state.id,
                    time_elapsed=state.time_elapsed,
                    metal=state.metal,
                    energy=state.energy)
    
    def __repr__(self):
        return f'COST {self.time_elapsed:.2f}s | {self.metal:.2f}m | {self.energy:.2f}e'