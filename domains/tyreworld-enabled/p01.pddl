(define (problem tyreworld-1)
(:domain tyreworld)
(:objects 
wrench1 wrench2 wrench3 jack1 jack2 jack3 pump1 pump2 pump3 - tool
the-hub1 - hub
nuts1 - nut
boot - container
r1 w1 - wheel
)
(:init
(in jack1 boot)
(in jack2 boot)
(in jack3 boot)
(in pump1 boot)
(in pump2 boot)
(in pump3 boot)
(in wrench1 boot)
(in wrench2 boot)
(in wrench3 boot)
(unlocked boot)
(closed boot)
(intact r1)
(in r1 boot)
(not-inflated r1)
(on w1 the-hub1)
(on-ground the-hub1)
(tight nuts1 the-hub1)
(fastened the-hub1)
)
(:goal
(and
(on r1 the-hub1)
(inflated r1)
(tight nuts1 the-hub1)
(in w1 boot)
(in wrench1 boot)
(in wrench2 boot)
(in wrench3 boot)
(in jack1 boot)
(in jack2 boot)
(in jack3 boot)
(in pump1 boot)
(in pump2 boot)
(in pump3 boot)
(closed boot)
)
)
)
