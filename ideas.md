increase timestep if there are fewer available actions

somehow limit worker swapping structures all the time, introduce swap build action? -> no need, build one thing with all builders at a time

the shortest path is time only, but resource storage is not really prioritized so right now we are prioritizing paths with the fastest possible entity acquisition ignoring the value of storing resources for the future. I think this is a reasonable tradeoff because of the 'spend your resources' principle in BAR and RTS in general

TODOS:

pruning via stalling (if stalling goes to bottom of prio q)

multiples doesnt work correctly for several blocks of the same type

command line args for logging

POP COMMANDER INTO SMALLER CHUNKS!!!!!!!

static delay, this would also help solve the iterative bonus of block building not showing up in the build order

early exit

update strings to be armturbine, corturbine etc.
    -pull unit data and strings from the github or a file

desired income

multiobjective should provide small improvements since you can use entities as a key and time,m,e as the 3 cost metrics it just is very small and not worth the computational cost to ensure optimality

-------

genetic algorithm or sim anneal may be a better approach, this probably would be benefited by a hand fed solution example, or an initial solution that just takes a very long and easy method to get to the goal. no longer proveably optimal but should work well and easy to multithread