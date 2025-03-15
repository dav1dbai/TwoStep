(define (problem gripper-3-2-4)
(:domain gripper-strips)
(:objects robot1 robot2 robot3 - robot
rgripper1 lgripper1 rgripper2 lgripper2 rgripper3 lgripper3 - gripper
room1 room2 - room
ball1 ball2 ball3 ball4 - object)
(:init
  (at-robby robot1 room1)
  (at-robby robot2 room1)
  (at-robby robot3 room1)
  (free robot1 rgripper1)
  (free robot1 lgripper1)
  (free robot2 rgripper2)
  (free robot2 lgripper2)
  (free robot3 rgripper3)
  (free robot3 lgripper3)
(at ball1 room2)
(at ball2 room2)
(at ball3 room2)
(at ball4 room2)
)
(:goal
(and
(at ball1 room2)
(at ball2 room1)
(at ball3 room1)
(at ball4 room1)
)
)
)