

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects robot1 robot2 robot3 robot4 robot5 - robot
    b1 b2 b3 b4 b5 - object )
(:init
(arm-empty robot1)
  (arm-empty robot2)
  (arm-empty robot3)
  (arm-empty robot4)
  (arm-empty robot5)
(on b1 b2)
(on b2 b3)
(on b3 b5)
(on b4 b1)
(on-table b5)
(clear b4)
)
(:goal
(and
(on b1 b3)
(on b3 b5))
)
)