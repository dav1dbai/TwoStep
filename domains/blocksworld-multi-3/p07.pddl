

(define (problem BW-rand-6)
(:domain blocksworld-4ops)
(:objects robot1 robot2 robot3 - robot
    b1 b2 b3 b4 b5 b6  - object)
(:init
(arm-empty robot1)
  (arm-empty robot2)
  (arm-empty robot3)
(on-table b1)
(on b2 b3)
(on b3 b1)
(on-table b4)
(on b5 b2)
(on-table b6)
(clear b4)
(clear b5)
(clear b6)
)
(:goal
(and
(on b3 b5)
(on b4 b3))
)
)