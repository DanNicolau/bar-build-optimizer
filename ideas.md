increase timestep if there are fewer available actions

somehow limit worker swapping structures all the time, introduce swap build action? -> no need, build one thing with all builders at a time

the shortest path is time only, but resource storage is not really prioritized so right now we are prioritizing paths with the fastest possible entity acquisition ignoring the value of storing resources for the future. I think this is a reasonable tradeoff because of the 'spend your resources' principle in BAR and RTS in general

TODOS:

reclaim + com det

reclaim_pool instead of commander wreck, we can increase the metal in the pool when things are set to be reclaimed

static delay, this would also help solve the iterative bonus of block building not showing up in the build order

reclaim_power ? lab buildings will have 0

pruning

early exit

might be better to have a buildable reserve which would create a new hash where some amount of stuff is saved before it is consumed in a later hash

why some goals negative e

known build heuristic ala A*

update strings to be armturbine, corturbine etc.