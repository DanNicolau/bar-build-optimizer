increase timestep if there are fewer available actions

somehow limit worker swapping structures all the time, introduce swap build action? -> no need, build one thing with all builders at a time

the shortest path is time only, but resource storage is not really prioritized so right now we are prioritizing paths with the fastest possible entity acquisition ignoring the value of storing resources for the future. I think this is a reasonable tradeoff because of the 'spend your resources' principle in BAR and RTS in general

TODOS:



multioptimization will go on forever because we can always get more metal..., trigger an end state as soon as goal is reached and only look for faster at that point -> move the code to a new file please
    ok so i think the part im fucking up on is that this doesnt have optimal substructure... we can't really use dijkstra's so we just to a BFS/DFS w/wo a heuristic and then prune based on domination by the solution states found

        ok feeling kind of stupid, we dont have optimal substructure so we can't apply this method....
        we just need to do good pruning, ill keep the code since its more general than we need and i dont think there's any downsides but man what a waste of time

    can do iterative deepening if memory becomes an issue

hash does not do well with reclaim, need to include metal as second cost metric and use a completely better criteria to remove a neighbour 

POP COMMANDER INTO SMALLER CHUNKS!!!!!!!

static delay, this would also help solve the iterative bonus of block building not showing up in the build order

pruning

early exit

known build heuristic ala A*

update strings to be armturbine, corturbine etc.
    -pull unit data and strings from the github or a file

desired income

