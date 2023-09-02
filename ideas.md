increase timestep if there are fewer available actions

somehow limit worker swapping structures all the time, introduce swap build action? -> no need, build one thing with all builders at a time

the shortest path is time only, but resource storage is not really prioritized so right now we are prioritizing paths with the fastest possible entity acquisition ignoring the value of storing resources for the future. I think this is a reasonable tradeoff because of the 'spend your resources' principle in BAR and RTS in general

TODOS:

turn off converters if energy is hitting 0

-------

genetic algorithm or sim anneal may be a better approach, this probably would be benefited by a hand fed solution example, or an initial solution that just takes a very long and easy method to get to the goal. no longer proveably optimal but should work well and easy to multithread