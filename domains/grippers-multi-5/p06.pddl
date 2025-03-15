(define (problem gripper-2-3-1)
(:domain gripper-strips)
(:objects robot1 robot2 robot3 robot4 robot5 - robot
rgripper1 lgripper1 rgripper2 lgripper2 rgripper3 lgripper3 rgripper4 lgripper4 rgripper5 lgripper5 - gripper
room1 room2 room3 - room
ball1 - object)
(:init
  (at-robby robot1 room1)
  (at-robby robot2 room1)
  (at-robby robot3 room1)
  (at-robby robot4 room1)
  (at-robby robot5 room1)
  (free robot1 rgripper1)
  (free robot1 lgripper1)
  (free robot2 rgripper2)
  (free robot2 lgripper2)
  (free robot3 rgripper3)
  (free robot3 lgripper3)
  (free robot4 rgripper4)
  (free robot4 lgripper4)
  (free robot5 rgripper5)
  (free robot5 lgripper5)
(at-robby robot1 room3)
(at-robby robot2 room2)
(at ball1 room1)
)
(:goal
(and
(at ball1 room3)
)
)
)