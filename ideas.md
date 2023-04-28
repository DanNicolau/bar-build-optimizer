increase timestep if there are fewer available actions

somehow limit worker swapping structures all the time, introduce swap build action? -> no need, build one thing with all builders at a time

the shortest path is time only, but resource storage is not really prioritized so right now we are prioritizing paths with the fastest possible entity acquisition ignoring the value of storing resources for the future. I think this is a reasonable tradeoff because of the 'spend your resources' principle in BAR and RTS in general

TODOS:

hash does not do well with reclaim, need to include metal as second cost metric and use a completely better criteria to remove a neighbour 

POP COMMANDER INTO SMALLER CHUNKS!!!!!!!

static delay, this would also help solve the iterative bonus of block building not showing up in the build order

pruning

early exit

known build heuristic ala A*

update strings to be armturbine, corturbine etc.

desired income