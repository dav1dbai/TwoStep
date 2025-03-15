

(define (problem BW-rand-6)
(:domain blocksworld-4ops)
(:objects robot1 robot2 robot3 - robot
    b1 b2 b3 b4 b5 b6  - object)
(:init
(arm-empty robot1)
  (arm-empty robot2)
  (arm-empty robot3)
(on b1 b3)
(on-table b2)
(on b3 b2)
(on b4 b5)
(on b5 b1)
(on b6 b4)
(clear b6)
)
(:goal
(and
(on b1 b6)
(on b3 b5)
(on b6 b2))
)
)