(define (problem gripper-4-3-6)
(:domain gripper-strips)
(:objects robot1 - robot
rgripper1 lgripper1 - gripper
room1 room2 room3 - room
ball1 ball2 ball3 ball4 ball5 ball6 - object)
(:init
(at-robby robot1 room3)
(free robot1 rgripper1)
(free robot1 lgripper1)
(at ball1 room2)
(at ball2 room2)
(at ball3 room1)
(at ball4 room3)
(at ball5 room3)
(at ball6 room3)
)
(:goal
(and
(at ball1 room1)
(at ball2 room1)
(at ball3 room2)
(at ball4 room3)
(at ball5 room3)
(at ball6 room3)
)
)
)
