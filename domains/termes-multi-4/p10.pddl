(define (problem termes-00112-0080-5x4x4-random_towers_5x4_4_2_13)
(:domain termes)
; termes-00112-0080-5x4x4-random_towers_5x4_4_2_13
; Initial state:
;  0   0  R0D  0   0 
;  0   0   0   0   0 
;  0   0   0   0   0 
;  0   0   0   0   0 
; Goal state:
;  0   0   0   2   0 
;  0   0   0   0   0 
;  0   0   0   0   0 
;  0   0   4   0   0 
; Maximal height: 4
(:objects
    n0 - numb
    n1 - numb
    n2 - numb
    n3 - numb
    n4 - numb
    pos-0-0 - position
    pos-0-1 - position
    pos-0-2 - position
    pos-0-3 - position
    pos-1-0 - position
    pos-1-1 - position
    pos-1-2 - position
    pos-1-3 - position
    pos-2-0 - position
    pos-2-1 - position
    pos-2-2 - position
    pos-2-3 - position
    pos-3-0 - position
    pos-3-1 - position
    pos-3-2 - position
    pos-3-3 - position
    pos-4-0 - position
    pos-4-1 - position
    pos-4-2 - position
    pos-4-3 - position
    robot1 robot2 robot3 robot4 - robot
)
(:init
    (height pos-0-0 n0)
    (height pos-0-1 n0)
    (height pos-0-2 n0)
    (height pos-0-3 n0)
    (height pos-1-0 n0)
    (height pos-1-1 n0)
    (height pos-1-2 n0)
    (height pos-1-3 n0)
    (height pos-2-0 n0)
    (height pos-2-1 n0)
    (height pos-2-2 n0)
    (height pos-2-3 n0)
    (height pos-3-0 n0)
    (height pos-3-1 n0)
    (height pos-3-2 n0)
    (height pos-3-3 n0)
    (height pos-4-0 n0)
    (height pos-4-1 n0)
    (height pos-4-2 n0)
    (height pos-4-3 n0)
    (at robot1 pos-2-0)
    (at robot2 pos-2-0)
    (at robot3 pos-2-0)
    (at robot4 pos-2-0)
    (SUCC n1 n0)
    (SUCC n2 n1)
    (SUCC n3 n2)
    (SUCC n4 n3)
    (NEIGHBOR pos-0-0 pos-1-0)
    (NEIGHBOR pos-0-0 pos-0-1)
    (NEIGHBOR pos-0-1 pos-1-1)
    (NEIGHBOR pos-0-1 pos-0-0)
    (NEIGHBOR pos-0-1 pos-0-2)
    (NEIGHBOR pos-0-2 pos-1-2)
    (NEIGHBOR pos-0-2 pos-0-1)
    (NEIGHBOR pos-0-2 pos-0-3)
    (NEIGHBOR pos-0-3 pos-1-3)
    (NEIGHBOR pos-0-3 pos-0-2)
    (NEIGHBOR pos-1-0 pos-0-0)
    (NEIGHBOR pos-1-0 pos-2-0)
    (NEIGHBOR pos-1-0 pos-1-1)
    (NEIGHBOR pos-1-1 pos-0-1)
    (NEIGHBOR pos-1-1 pos-2-1)
    (NEIGHBOR pos-1-1 pos-1-0)
    (NEIGHBOR pos-1-1 pos-1-2)
    (NEIGHBOR pos-1-2 pos-0-2)
    (NEIGHBOR pos-1-2 pos-2-2)
    (NEIGHBOR pos-1-2 pos-1-1)
    (NEIGHBOR pos-1-2 pos-1-3)
    (NEIGHBOR pos-1-3 pos-0-3)
    (NEIGHBOR pos-1-3 pos-2-3)
    (NEIGHBOR pos-1-3 pos-1-2)
    (NEIGHBOR pos-2-0 pos-1-0)
    (NEIGHBOR pos-2-0 pos-3-0)
    (NEIGHBOR pos-2-0 pos-2-1)
    (NEIGHBOR pos-2-1 pos-1-1)
    (NEIGHBOR pos-2-1 pos-3-1)
    (NEIGHBOR pos-2-1 pos-2-0)
    (NEIGHBOR pos-2-1 pos-2-2)
    (NEIGHBOR pos-2-2 pos-1-2)
    (NEIGHBOR pos-2-2 pos-3-2)
    (NEIGHBOR pos-2-2 pos-2-1)
    (NEIGHBOR pos-2-2 pos-2-3)
    (NEIGHBOR pos-2-3 pos-1-3)
    (NEIGHBOR pos-2-3 pos-3-3)
    (NEIGHBOR pos-2-3 pos-2-2)
    (NEIGHBOR pos-3-0 pos-2-0)
    (NEIGHBOR pos-3-0 pos-4-0)
    (NEIGHBOR pos-3-0 pos-3-1)
    (NEIGHBOR pos-3-1 pos-2-1)
    (NEIGHBOR pos-3-1 pos-4-1)
    (NEIGHBOR pos-3-1 pos-3-0)
    (NEIGHBOR pos-3-1 pos-3-2)
    (NEIGHBOR pos-3-2 pos-2-2)
    (NEIGHBOR pos-3-2 pos-4-2)
    (NEIGHBOR pos-3-2 pos-3-1)
    (NEIGHBOR pos-3-2 pos-3-3)
    (NEIGHBOR pos-3-3 pos-2-3)
    (NEIGHBOR pos-3-3 pos-4-3)
    (NEIGHBOR pos-3-3 pos-3-2)
    (NEIGHBOR pos-4-0 pos-3-0)
    (NEIGHBOR pos-4-0 pos-4-1)
    (NEIGHBOR pos-4-1 pos-3-1)
    (NEIGHBOR pos-4-1 pos-4-0)
    (NEIGHBOR pos-4-1 pos-4-2)
    (NEIGHBOR pos-4-2 pos-3-2)
    (NEIGHBOR pos-4-2 pos-4-1)
    (NEIGHBOR pos-4-2 pos-4-3)
    (NEIGHBOR pos-4-3 pos-3-3)
    (NEIGHBOR pos-4-3 pos-4-2)
    (IS-DEPOT pos-2-0)
)
(:goal (and
    (height pos-0-0 n0)
    (height pos-0-1 n0)
    (height pos-0-2 n0)
    (height pos-0-3 n0)
    (height pos-1-0 n0)
    (height pos-1-1 n0)
    (height pos-1-2 n0)
    (height pos-1-3 n0)
    (height pos-2-0 n0)
    (height pos-2-1 n0)
    (height pos-2-2 n0)
    (height pos-2-3 n4)
    (height pos-3-0 n2)
    (height pos-3-1 n0)
    (height pos-3-2 n0)
    (height pos-3-3 n0)
    (height pos-4-0 n0)
    (height pos-4-1 n0)
    (height pos-4-2 n0)
    (height pos-4-3 n0)
    (not (has-block robot1))
    (not (has-block robot2))
    (not (has-block robot3))
    (not (has-block robot4))
))
)