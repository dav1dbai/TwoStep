

(define (problem BW-rand-3)
(:domain blocksworld-4ops)
(:objects robot1 robot2 robot3 robot4 - robot
    b1 b2 b3 - object )
(:init
(arm-empty robot1)
  (arm-empty robot2)
  (arm-empty robot3)
  (arm-empty robot4)
(on b1 b3)
(on-table b2)
(on b3 b2)
(clear b1)
)
(:goal
(and
(on b2 b3)
(on b3 b1))
)
)