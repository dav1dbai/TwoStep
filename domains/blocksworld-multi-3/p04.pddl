

(define (problem BW-rand-4)
(:domain blocksworld-4ops)
(:objects robot1 robot2 robot3 - robot
    b1 b2 b3 b4 - object )
(:init
(arm-empty robot1)
  (arm-empty robot2)
  (arm-empty robot3)
(on b1 b4)
(on-table b2)
(on b3 b1)
(on b4 b2)
(clear b3)
)
(:goal
(and
(on b1 b2)
(on b2 b3)
(on b3 b4))
)
)